"""
Main application routes.
"""
from flask import Blueprint, render_template, request, flash, redirect, url_for
from flask_login import login_required, current_user
from .models import User, db, MetricLogs
from .netdata_utils import get_metrics_from_url
from functools import wraps

main_bp = Blueprint('main', __name__)

@main_bp.route('/')
def index():
    """Render the login page."""
    return render_template('login.html')

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if current_user.type != 'Admin':
            return redirect(url_for('main.unauthorized'))
        return f(*args, **kwargs)
    return decorated_function

@main_bp.route('/dashboard')
@login_required
def dashboard():
    """Render real-time dashboard for all machines."""
    from app.netdata_utils import get_metrics_from_url
    MACHINES = {
        "local": "http://192.155.91.125:19999",
        "node1": "http://66.175.212.234:19999",
        "node2": "http://97.107.138.34:19999",
        "node3": "http://97.107.128.46:19999"
    }

    all_data = {}

    for name, url in MACHINES.items():
        try:
            all_data[name] = get_metrics_from_url(url)
        except Exception as e:
            all_data[name] = {"error": str(e)}

    return render_template('dashboard.html', all_data=all_data)

@main_bp.route('/unauthorized')
def unauthorized():
    """Render the unauthorized access page."""
    return render_template('unauthorized.html')

@main_bp.route('/manage_users', methods=['GET', 'POST'])
@login_required
@admin_required
def manage_users():
    if request.method == 'POST':
        if 'delete_email' in request.form:
            email = request.form.get('delete_email')
            if current_user.email == email:
                flash("You cannot delete your own account while logged in.", "danger")
            else:
                user = User.query.filter_by(email=email).first()
                if user:
                    db.session.delete(user)
                    db.session.commit()
                    flash(f'User {email} deleted.', 'success')
                else:
                    flash(f'User {email} not found.', 'warning')
        else:
            email = request.form.get('email')
            user_type = request.form.get('user_type', 'User')
            if email:
                user = User.query.filter_by(email=email).first()
                if user:
                    user.type = user_type
                else:
                    user = User(username=email.split('@')[0], email=email, type=user_type)
                    db.session.add(user)
                db.session.commit()
                flash('User updated successfully.', 'success')

    users = User.query.all()
    return render_template('manage_users.html', users=users)


@main_bp.route('/history')
@login_required
@admin_required
def history():
    logs = MetricLogs.query.order_by(MetricLogs.timestamp.desc()).limit(200).all()
    logs.reverse()

    from collections import defaultdict
    machine_logs = defaultdict(list)
    for log in logs:
        machine_logs[log.machine_name].append({
            "timestamp": log.timestamp.isoformat(),
            "cpu_usage": log.cpu_usage,
            "memory_usage": log.memory_usage,
            "disk_usage": log.disk_usage,
            "network_usage": log.network_usage
        })

    return render_template('history.html', machine_logs=machine_logs)

