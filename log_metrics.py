import requests
from datetime import datetime, timezone
from run import app
from app.models import db, MetricLogs

MACHINES = {
    "local": "http://192.155.91.125:19999",
    "node1": "http://66.175.212.234:19999",
    "node2": "http://97.107.138.34:19999",
    "node3": "http://97.107.128.46:19999"
}

def get_metrics(base_url):
    base = f"{base_url}/api/v1/data?after=-60&points=1&group=average"

    def fetch(chart, key):
        url = f"{base}&chart={chart}"
        r = requests.get(url, timeout=5)
        r.raise_for_status()
        data = r.json()
        labels = data["labels"]
        row = data["data"][-1]
        return row[labels.index(key)]

    return {
        "cpu": fetch("system.cpu", "user"),
        "memory": fetch("system.ram", "used"),
        "disk": fetch("disk_space./", "used"),
        "network": fetch("system.net", "received")
    }

with app.app_context():
    for name, url in MACHINES.items():
        try:
            metrics = get_metrics(url)
            log = MetricLogs(
                machine_name=name,
                timestamp=datetime.now(timezone.utc),
                cpu_usage=metrics["cpu"],
                memory_usage=metrics["memory"],
                disk_usage=metrics["disk"],
                network_usage=metrics["network"]
            )
            db.session.add(log)
            print(f"Logged for {name} at {log.timestamp}")
        except Exception as e:
            print(f"Failed to log for {name}: {e}")

    db.session.commit()
