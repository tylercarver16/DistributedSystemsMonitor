# Distributed Systems Monitor

A secure, web-based distributed systems monitoring platform built with **Flask**, **Netdata**, and **Gunicorn**, designed to collect, log, and visualize system metrics across a **five-machine cluster**.

This project was developed incrementally across multiple course phases, covering system security hardening, secure web deployment, and distributed monitoring.

---

## Overview

The Distributed Systems Monitor provides:

- Real-time monitoring of CPU, memory, disk, and network usage  
- Historical analysis using metrics logged at fixed intervals  
- Role-based access control (RBAC) distinguishing Admin and User privileges  
- Secure, production-style deployment using Gunicorn, Nginx, and HTTPS  
- Fault tolerance when cluster nodes are unreachable  

The system was deployed live at **tcarver.me** and later archived to avoid ongoing hosting costs. Screenshots and documentation are included to preserve proof of functionality.

---

## Architecture

### High-Level Components

#### Flask Application
- Central controller for the system
- Handles authentication and RBAC enforcement
- Aggregates metrics and renders dashboards

#### Netdata Agents (5 Machines)
- Each machine runs a Netdata agent
- Metrics exposed via HTTP API
- API access restricted to cluster members only

#### Database
- Stores timestamped metrics at 10-minute intervals
- Supports historical trend queries

#### Deployment Stack
- **Gunicorn** – WSGI application server  
- **Nginx** – Reverse proxy and HTTPS termination  
- **Unix socket** – Inter-process communication  
- **Certbot** – TLS certificate management  

---

## Features

### Distributed Monitoring
- Collects metrics from five machines in a cluster
- Uses Netdata APIs to retrieve:
  - CPU usage
  - Memory usage
  - Disk usage
  - Network activity

### Logging & Historical Data
- Metrics logged every **10 minutes**
- Historical trends viewable over multiple days
- Database queries optimized for **< 1 second** frontend response time

### Role-Based Access Control (RBAC)

**Admin**
- View real-time metrics
- View historical metrics
- Full cluster visibility

**User**
- View real-time metrics only

Unauthorized access redirects users to a dedicated error page.

### Fault Tolerance
- Handles unreachable machines gracefully
- Logs errors and stores `NULL` values in the database
- Continues monitoring remaining nodes without crashing

---

## Security Foundations

This project builds on earlier phases focused on security and deployment.

### Project Part 1 – System Hardening
- Ubuntu 24.04 server hardened using **Lynis**
- Key-based SSH authentication enforced
- Password-based SSH authentication disabled
- Improved system hardening index

### Project Part 2 – Secure Web Deployment
- Python **3.13** compiled from source (`/opt/python3`)
- Custom WSGI server (`unicorn.py`) implemented for learning purposes
- HTTPS enforced using **Certbot**
- Firewall configured to restrict exposed ports
- SSH moved to a non-standard port

---

## WSGI Server Evolution

This project demonstrates progression from low-level understanding to production tooling.

1. **Custom WSGI Server (`unicorn.py`)**
   - Implemented in Project Part 2
   - Provided hands-on experience with socket-based request handling and the WSGI interface

2. **Gunicorn**
   - Adopted in Project Part 3
   - Production-grade WSGI server
   - Uses the same Nginx + Unix socket architecture

---

## Screenshots

Screenshots captured during live deployment are available in:

```
docs/screenshots/
```

They demonstrate:
- Google OAuth login
- RBAC enforcement (Admin vs User)
- Real-time monitoring dashboard
- Historical metrics visualization
- Handling of unreachable cluster nodes
- HTTPS-enabled deployment

---

## Running Locally

### Prerequisites
- Python 3.13+
- Netdata (optional for local testing)

### Setup

```bash
/opt/python3/bin/python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

### Run (Development)

```bash
python run.py
```

### Run with Gunicorn (Production-Style)

```bash
./venv/bin/gunicorn --workers 4 --bind unix:/tmp/flask.sock run:app
```

> Gunicorn must be executed from within the virtual environment to avoid conflicts with system-wide Python installations.

---

## Logs & Database

- Runtime logs are excluded from version control
- A sample log is included for reference:

```
logs/sample_metric.log
```

## Repository Structure

```
cop4521-flask/
├── app/
│   ├── auth.py
│   ├── admin.py
│   ├── routes.py
│   ├── models.py
│   ├── netdata_utils.py
│   ├── static/
│   └── templates/
├── docs/
│   └── screenshots/
├── tests/
├── log_metrics.py
├── run.py
├── requirements.txt
├── README.md
└── LICENSE
```

---

## Project Status

This project was fully deployed and demonstrated on a production server.  
The live instance was intentionally shut down after course completion to avoid hosting costs.

All functionality is preserved through:
- Source code
- Documentation
- Screenshots

---

## Skills Demonstrated

- Distributed systems monitoring
- Secure Linux server administration
- Flask application architecture
- Netdata API integration
- Role-based access control
- Production deployment (Gunicorn + Nginx + HTTPS)
- Fault-tolerant system design
- Clean Git and documentation practices
