# RDRS — Security Monitoring & Incident Detection Platform

RDRS is a Python-based security monitoring and incident detection platform.

It monitors filesystem activity, detects suspicious behavior, calculates threat
scores, creates security incidents, collects evidence, and provides a web
dashboard for security monitoring.

## Features

- Real-time file activity monitoring
- Suspicious event detection
- Entropy-based analysis
- Threat scoring
- Incident management
- Evidence collection
- Incident timelines
- Incident resolution and reopening
- REST API
- Web security dashboard
- JSON security reports
- CSV security reports
- SQLite database
- Configurable detection thresholds
- Linux systemd deployment

## Current RDRS Features

- File-system monitoring with Watchdog
- Shannon entropy analysis using 64 KB samples
- Sliding-window ransomware activity detection
- Rapid file modification detection
- Mass rename detection
- High-entropy detection
- Process telemetry using psutil
- CPU and memory telemetry
- Process executable and parent-process tracking
- Detection scoring with configurable thresholds
- Normal / Warning / Critical severity levels
- Incident persistence using SQLite
- Evidence tracking and quarantine copying
- Safe file scanner with SHA-256 analysis
- Suspicious-extension and ransomware-keyword indicators
- Scanner upload endpoint
- Scanner incoming/quarantine storage visibility
- Incident and event REST APIs
- JSON and CSV reporting
- Dashboard File Scanner navigation
- Dashboard scanner storage visibility
- Simulation/safe-response architecture
