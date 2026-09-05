[![RDRS CI](https://github.com/Raheem-ali2763/rdrs-security-monitor/actions/workflows/ci.yml/badge.svg)](https://github.com/Raheem-ali2763/rdrs-security-monitor/actions/workflows/ci.yml)

# RDRS — Security Monitoring & Incident Detection Platform

> **Live Production Deployment:** https://rdrs-dusky.vercel.app

RDRS (Ransomware Detection & Response System) is a Python-based defensive security monitoring and incident detection platform designed to monitor filesystem activity, identify suspicious behavior, calculate threat scores, create security incidents, collect evidence, scan files, and provide a web dashboard for security monitoring.

The system is designed for defensive cybersecurity research, detection engineering, incident-response experimentation, and controlled security testing.

---

## Live Deployment

The current RDRS web application is deployed on Vercel.

**Production Dashboard:**  
https://rdrs-dusky.vercel.app

**GitHub Repository:**  
https://github.com/Raheem-ali2763/rdrs-security-monitor

---

## Overview

RDRS combines real-time filesystem monitoring, entropy-based analysis, event detection, process telemetry, behavioral activity analysis, threat scoring, incident management, evidence collection, file scanning, REST APIs, and a web-based security dashboard into a single security monitoring platform.

The system observes configured filesystem activity and processes detected events through a detection pipeline. Suspicious activity is evaluated using configurable detection rules and threat-scoring weights. When activity reaches the required severity, RDRS can create and manage a security incident.

---

## Features

- Real-time filesystem activity monitoring
- Suspicious event detection
- Entropy-based file analysis
- Shannon entropy analysis with bounded file sampling
- Process telemetry using `psutil`
- Rolling filesystem activity analysis
- Rapid file modification detection
- Mass rename detection
- Extension-change detection
- Threat scoring
- Configurable detection thresholds
- Security incident creation and management
- Incident status management
- Incident timelines
- Evidence collection
- SHA-256 evidence hashing
- Event repository
- REST API
- Web-based security dashboard
- File scanner
- Scanner risk scoring
- Suspicious filename and extension detection
- Scanner entropy analysis
- Scanner SHA-256 analysis
- Critical scanner incident creation
- Evidence/quarantine handling
- Security settings management
- JSON security reports
- CSV security reports
- Local service deployment with systemd
- Production web deployment with Vercel
- Automated unit test suite

---

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
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
       ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
       │   Entropy   │  │ File Activity│  │   Process   │
       │   Analysis  │  │   Detection  │  │  Telemetry  │
       └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
              │                │                │
              └────────────────┼────────────────┘
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
                            │ Yes
                            ▼
                   ┌──────────────────────┐
                   │ Incident Management │
                   └──────────┬───────────┘
                              │
               ┌──────────────┼────────────────┐
               ▼              ▼                ▼
        ┌───────────┐   ┌────────────┐   ┌────────────┐
        │ Evidence  │   │  Timeline  │   │ Repository │
        └───────────┘   └────────────┘   └────────────┘
                              │
                              ▼
                    ┌─────────────────────┐
                    │      REST API       │
                    └──────────┬──────────┘
                               │
                  ┌────────────┴─────────────┐
                  ▼                          ▼
         ┌─────────────────┐        ┌─────────────────┐
         │ RDRS Dashboard  │        │ Security Reports│
         └─────────────────┘        └─────────────────┘
Detection Pipeline

The detection pipeline processes filesystem activity through multiple stages:

Filesystem events are collected by the monitoring layer.
Events are normalized and passed to the detection pipeline.
Entropy analysis evaluates suspicious file characteristics.
File activity rules evaluate rapid modifications, renames, and related activity.
Process telemetry provides CPU, memory, disk-write, executable, and parent-process information.
Behavioral activity is evaluated over a rolling time window.
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

The final threat score is capped at 100.

Severity Levels
Score	Severity
0–40	Normal
40–70	Warning
70–100	Critical

Severity thresholds are configurable through config.yaml.

levels:
  normal_max: 40
  warning_max: 70
  critical_max: 100
File Scanner

RDRS includes a dedicated file scanner for analyzing individual files without executing them.

The scanner provides:

SHA-256 hashing
Shannon entropy analysis
Bounded file sampling
Suspicious extension detection
Suspicious filename detection
Encryption-related indicators
Risk scoring
Severity classification
Detection reasons
Incident creation for critical findings
Evidence collection
Quarantine/evidence-copy handling
Scanner Analysis

The scanner evaluates indicators including:

High entropy
Ransomware-related extensions
Suspicious filenames
Encryption-related patterns

The resulting scanner risk score is capped at 100.

Critical findings can create an incident and preserve evidence for investigation.

Original files are not modified during evidence collection.

Security Dashboard

The RDRS dashboard provides a centralized interface for security monitoring.

Dashboard functionality includes:

Threat score
Events
Suspicious events
Recent activity
Active incidents
Incident details
Evidence
Response actions
Reports
Settings
File Scanner
Scanner results
Scanner storage information
Security monitoring status

The dashboard provides visibility into recorded activity, suspicious events, incidents, evidence, scanner findings, and report generation.

Production Dashboard

https://rdrs-dusky.vercel.app

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

Critical detections can generate incidents containing:

Incident ID
Severity
Threat score
Summary
Start/end timestamps
Affected files
Evidence records
SHA-256 hashes
Evidence Collection

For detected incidents, RDRS can associate evidence with the incident record.

Evidence can be retrieved through the API and displayed through the dashboard.

Evidence collection is designed to preserve investigation artifacts without modifying the original files.

Security Reports

RDRS supports security report generation in two formats:

JSON
/api/reports/{incident_ref}/json
CSV
/api/reports/{incident_ref}/csv

Reports can contain incident information and supporting security data such as:

Timelines
Evidence
Affected files
Suspicious processes
Events
Recommendations where available
REST API

RDRS exposes REST endpoints through FastAPI.

Core API Areas
Area	Purpose
Health	Service health
Status	System status
Events	Security event retrieval and statistics
Incidents	Incident creation and management
Evidence	Incident evidence management
Response	Incident resolve/reopen operations
Reports	JSON and CSV security reports
Service	Monitoring service control and status
Settings	Security monitoring configuration
Scan	File scanning and scanner storage
Common Endpoints
Method	Endpoint	Purpose
GET	/health	Service health
GET	/status	System status
GET	/alerts	Security alerts
GET	/events	Filesystem events
GET	/reports	Reports
POST	/scan	File scanning
POST	/settings	Configuration updates

FastAPI interactive documentation is available at:

http://127.0.0.1:8000/docs

when running locally.

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
│   │       ├── scan.py
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
│   │   ├── activity_window.py
│   │   ├── base.py
│   │   ├── engine.py
│   │   ├── entropy_detector.py
│   │   ├── file_monitor.py
│   │   ├── incident_callback.py
│   │   ├── pipeline.py
│   │   ├── process_service.py
│   │   ├── process_telemetry.py
│   │   └── service.py
│   │
│   ├── reports/
│   ├── scanner/
│   │   ├── analyzer.py
│   │   ├── models.py
│   │   └── scanner.py
│   │
│   ├── web/
│   │   ├── dashboard.py
│   │   ├── scanner_page.py
│   │   └── templates/
│   │
│   └── main.py
│
├── tests/
│   ├── unit/
│   └── integration/
│
├── data/
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
Vercel
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
Scanner configuration
Running the Application

Start RDRS with:

./run_rdrs.sh

The application runs locally on:

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
Production Web Deployment

The current web deployment is available through Vercel:

https://rdrs-dusky.vercel.app

The production deployment provides access to the RDRS web interface.

Testing

The project includes automated tests covering major application components.

Current Test Status

The latest test suite passes successfully:

40 passed, 10 warnings

The warnings are deprecation warnings and do not represent test failures.

Run the test suite:

pytest -q

Compile-check the application:

python -m compileall -q app

Optional coverage:

pytest --cov=app
Safe Testing & Security Scope

RDRS is a defensive cybersecurity project.

Testing should use:

Dedicated sandbox directories
Throwaway files
Controlled filesystem activity
Safe simulation scenarios

RDRS does not require real ransomware or malware to be executed for testing.

The project is intended for:

Security research
Defensive monitoring
Detection engineering
Incident-response experimentation
Cybersecurity education

Do not use the system to execute, distribute, or develop real malware.

Runtime Data

Runtime databases and generated reports are intentionally excluded from version control.

The repository ignores local runtime artifacts such as:

*.db
*.sqlite
logs/
.pytest_cache/
.coverage
data/reports/*
data/scanner/*
data/quarantine/*
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
API exposure
Evidence storage permissions
Current Deployment Status

RDRS currently supports:

Local security monitoring
Filesystem event detection
File entropy analysis
Process telemetry
Behavioral activity analysis
Threat scoring
Incident management
Evidence collection
File scanning
Security dashboard
REST APIs
SQLite persistence
Automated testing
Local systemd service deployment
Production Vercel deployment
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
Improved alert integrations
Expanded detection coverage
Version

Current release:

v0.1.0
License

This project is licensed under the MIT License.

See the LICENSE file for details.

Author

Raheem Ali

Cybersecurity / Security Engineering Project

GitHub:

https://github.com/Raheem-ali2763
