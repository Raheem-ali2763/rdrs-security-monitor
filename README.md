# RDRS — Security Monitoring & Incident Detection Platform

RDRS is a Python-based security monitoring and incident detection platform designed to monitor filesystem activity, identify suspicious behavior, calculate threat scores, create security incidents, collect evidence, and provide a web dashboard for security monitoring.

## Overview

RDRS combines real-time filesystem monitoring, entropy-based analysis, event detection, threat scoring, incident management, evidence collection, REST APIs, and a web-based security dashboard into a single security monitoring platform.

The system continuously observes configured filesystem activity and processes detected events through a detection pipeline. Suspicious activity is evaluated using configurable detection rules and threat-scoring weights. When activity reaches the required severity, RDRS creates and manages a security incident.

## Features

- Real-time filesystem activity monitoring
- Suspicious event detection
- Entropy-based file analysis
- Threat scoring
- Security incident creation and management
- Incident status management
- Evidence collection
- Incident timelines
- Event repository
- REST API
- Web-based security dashboard
- Security settings management
- JSON security reports
- CSV security reports
- Local service deployment with systemd
- Automated unit test suite

## System Architecture

```text
                    ┌─────────────────────┐
                    │   Monitored Files   │
                    │   /data/sandbox     │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │   File Monitor      │
                    │   Watchdog Events   │
                    └──────────┬──────────┘
                               │
                               ▼
                    ┌─────────────────────┐
                    │ Detection Pipeline  │
                    └──────────┬──────────┘
                               │
             ┌─────────────────┼─────────────────┐
             ▼                 ▼                 ▼
      ┌─────────────┐   ┌─────────────┐   ┌─────────────┐
      │   Entropy   │   │ File Activity│   │   Process   │
      │   Analysis  │   │   Detection  │   │  Detection  │
      └──────┬──────┘   └──────┬──────┘   └──────┬──────┘
             │                 │                 │
             └─────────────────┼─────────────────┘
                               ▼
                    ┌─────────────────────┐
                    │    Threat Scoring   │
                    └──────────┬──────────┘
                               │
                               ▼
                     ┌──────────────────┐
                     │ Incident Required│
                     │        ?         │
                     └───────┬──────────┘
                         Yes │
                             ▼
                  ┌──────────────────────┐
                  │ Incident Management │
                  └──────────┬───────────┘
                             │
             ┌───────────────┼────────────────┐
             ▼               ▼                ▼
       ┌───────────┐   ┌────────────┐   ┌────────────┐
       │ Evidence  │   │  Timeline  │   │ Repository │
       └───────────┘   └────────────┘   └────────────┘
                             │
                             ▼
                    ┌─────────────────────┐
                    │      REST API       │
                    └──────────┬──────────┘
                               │
                 ┌─────────────┴─────────────┐
                 ▼                           ▼
        ┌─────────────────┐         ┌─────────────────┐
        │ RDRS Dashboard  │         │ Security Reports│
        └─────────────────┘         └────────┬────────┘
                                             │
                                      ┌──────┴──────┐
                                      ▼             ▼
                                   JSON          CSVDetection Pipeline

The detection pipeline processes filesystem activity through multiple stages:

Filesystem events are collected by the monitoring layer.
Events are normalized and passed to the detection pipeline.
Entropy analysis evaluates suspicious file characteristics.
File activity rules evaluate rapid modifications, renames, and related activity.
Process-related indicators can contribute to detection.
Detection results are converted into threat-score contributions.
The resulting threat score determines the severity of the activity.
Significant activity can result in a security incident.
Evidence and timeline information are associated with the incident.
Incident information becomes available through the REST API and dashboard.
Threat Scoring

RDRS uses configurable scoring weights to evaluate suspicious activity.

Detection Indicator	Score
Rapid file modification	40
Mass rename	30
High entropy	25
CPU spike	15
Unknown process	10

Severity levels are configurable through config.yaml.

levels:
  normal_max: 40
  warning_max: 70
  critical_max: 100
Incident Management

RDRS provides APIs for managing the complete incident lifecycle.

Supported operations include:

Listing incidents
Creating incidents
Viewing individual incidents
Updating incidents
Deleting incidents
Managing incident evidence
Viewing complete incident information
Updating incident status
Resolving incidents
Reopening incidents
Evidence Collection

For detected incidents, RDRS can associate evidence with the incident record.

Evidence can be retrieved through the API and displayed through the dashboard.

Security Dashboard

The RDRS dashboard provides a centralized interface for security monitoring.

Dashboard sections include:

Overview
Events
Incidents
Evidence
Reports
Settings
Security monitoring status

The dashboard provides visibility into recorded activity, suspicious events, incidents, evidence, and report generation.

Security Reports

RDRS supports security report generation in two formats:

JSON
/api/reports/{incident_ref}/json
CSV
/api/reports/{incident_ref}/csv

Reports contain incident information and supporting security data such as timelines, evidence, affected files, suspicious processes, events, and recommendations where available.

REST API

Main API areas include:

Area	Purpose
Events	Security event retrieval and statistics
Incidents	Incident creation and management
Evidence	Incident evidence management
Response	Incident resolve/reopen operations
Reports	JSON and CSV security reports
Service	Monitoring service control and status
Settings	Security monitoring configuration
Project Structure
rdrs-security-monitor/
│
├── app/
│   ├── api/
│   │   └── routes/
│   │       ├── events.py
│   │       ├── incidents.py
│   │       ├── reports.py
│   │       ├── response.py
│   │       ├── service.py
│   │       └── settings.py
│   │
│   ├── core/
│   │   ├── config.py
│   │   └── entropy.py
│   │
│   ├── database/
│   │   ├── incident_models.py
│   │   ├── models.py
│   │   ├── repository.py
│   │   └── session.py
│   │
│   ├── detectors/
│   │   ├── base.py
│   │   ├── engine.py
│   │   ├── entropy_detector.py
│   │   ├── file_monitor.py
│   │   ├── incident_callback.py
│   │   ├── pipeline.py
│   │   └── service.py
│   │
│   ├── reports/
│   ├── response/
│   ├── dashboard/
│   ├── web/
│   │   └── dashboard.py
│   │
│   └── main.py
│
├── tests/
│   └── unit/
│
├── data/
│   └── reports/
│
├── config.yaml
├── requirements.txt
├── run_rdrs.sh
├── .gitignore
└── README.md
Technologies Used
Python
FastAPI
SQLAlchemy
SQLite
Pydantic
Uvicorn
Watchdog
psutil
PyYAML
Loguru
ReportLab
Pytest
HTML/CSS/JavaScript
Installation

Clone the repository:

git clone https://github.com/Raheem-ali2763/rdrs-security-monitor.git
cd rdrs-security-monitor

Create a virtual environment:

python3 -m venv .venv
source .venv/bin/activate

Install dependencies:

pip install -r requirements.txt
Configuration

RDRS configuration is stored in:

config.yaml

The configuration controls:

Monitored paths
Recursive monitoring
Entropy analysis
Detection thresholds
File activity thresholds
Process thresholds
Threat-scoring weights
Severity levels
Database configuration
Logging configuration
Running the Application

Start RDRS with:

./run_rdrs.sh

The application runs on:

http://127.0.0.1:8000

FastAPI documentation:

http://127.0.0.1:8000/docs
Service Deployment

RDRS can run as a user-level systemd service.

Check service status:

systemctl --user status rdrs.service

Start the service:

systemctl --user start rdrs.service

Stop the service:

systemctl --user stop rdrs.service

Enable automatic startup:

systemctl --user enable rdrs.service
Testing

The project includes unit tests covering major components.

Run the test suite:

pytest

Run with coverage:

pytest --cov=app
Runtime Data

Runtime databases and generated reports are intentionally excluded from version control.

The repository ignores local runtime artifacts such as:

*.db
*.sqlite
logs/
.pytest_cache/
.coverage
data/reports/*
.venv/
Security Considerations

RDRS is intended for defensive security monitoring and analysis.

Before production deployment, administrators should review:

Monitored paths
File permissions
Database permissions
Network exposure
Authentication requirements
Logging configuration
Alerting requirements
Current Deployment

RDRS has been configured for local service deployment using systemd and can run as a persistent user service.

The repository contains the application source code, tests, configuration, startup script, and documentation required to reproduce the development environment.

Limitations

RDRS is currently a local security monitoring platform and should not be considered a complete enterprise SIEM or endpoint detection and response solution.

Production environments may require:

Authentication and authorization
Centralized logging
Distributed monitoring
Alert notifications
Secure remote agents
Persistent event streaming
Production database infrastructure
TLS configuration
Advanced process attribution
Future Improvements

Potential future improvements include:

User authentication and role-based access control
Email and webhook alerting
Centralized event collection
Additional detection rules
Machine-learning-assisted detection
Advanced process analysis
Multi-host monitoring
Container deployment
Production database support
Enhanced dashboard analytics
Version

Current release:

v0.1.0
License

This project is licensed under the MIT License.

See the LICENSE file for details.
Author

Raheem Ali
GitHub:

https://github.com/Raheem-ali2763
