# RDRS Architecture

## System Architecture

RDRS is organized as a real-time security monitoring and incident detection pipeline.

```mermaid
flowchart TD
    A[Monitored Filesystem] --> B[File Monitor]
    B --> C[File Activity Events]

    C --> D[Detection Pipeline]

    D --> E[Entropy Analysis]
    D --> F[File Activity Analysis]
    D --> G[Process Analysis]

    E --> H[Detection Engine]
    F --> H
    G --> H

    H --> I[Threat Scoring]

    I --> J{Incident Required?}

    J -->|No| K[Security Event]
    J -->|Yes| L[Incident Detection]

    L --> M[Evidence Collection]
    L --> N[Incident Timeline]
    L --> O[Incident Repository]

    M --> O
    N --> O

    K --> P[Event Repository]
    O --> Q[RDRS REST API]
    P --> Q

    Q --> R[RDRS Dashboard]
    Q --> S[Security Reports]

    S --> T[JSON Report]
    S --> U[CSV Report]

    R --> V[Events]
    R --> W[Incidents]
    R --> X[Evidence]
    R --> Y[Settings]
    R --> Z[Security Reports]
```

## Detection Pipeline

The core detection pipeline processes filesystem activity through multiple analysis stages:

```text
Monitored Files
      |
      v
File Activity Monitor
      |
      v
Security Events
      |
      v
Detection Pipeline
      |
      +----> Entropy Analysis
      |
      +----> File Activity Analysis
      |
      +----> Process Analysis
      |
      v
Detection Engine
      |
      v
Threat Scoring
      |
      v
Incident Decision
      |
      +---- No ----> Security Event
      |
      +---- Yes ---> Incident
                       |
                       +----> Evidence
                       |
                       +----> Timeline
                       |
                       +----> Incident Repository
```

## Main Components

### File Monitoring

Monitors configured filesystem paths and generates events for relevant file activity.

### Detection Engine

Combines multiple detection indicators and evaluates suspicious behavior.

### Entropy Analysis

Analyzes file entropy to identify potentially suspicious high-entropy file activity.

### Threat Scoring

Combines detection indicators using configured scoring weights to determine the severity of suspicious activity.

### Incident Detection

Converts significant suspicious activity into security incidents and maintains incident state.

### Evidence Collection

Stores relevant evidence associated with detected incidents.

### Incident Timeline

Maintains a chronological record of incident-related activity.

### REST API

The FastAPI-based REST API provides access to events, incidents, evidence, reports, settings, and monitoring controls.

### Dashboard

The web dashboard provides a security monitoring interface for:

- Events
- Incidents
- Evidence
- Settings
- Security Reports

### Security Reports

RDRS provides incident reports in:

- JSON format
- CSV format

## Data Flow

```text
Filesystem Activity
        |
        v
Event Generation
        |
        v
Detection Pipeline
        |
        v
Threat Analysis
        |
        v
Threat Score
        |
        v
Incident Decision
        |
        +------------------+
        |                  |
        v                  v
     Event             Incident
                           |
                           v
                    Evidence + Timeline
                           |
                           v
                    Incident Repository
                           |
                           v
                       REST API
                           |
              +------------+------------+
              |                         |
              v                         v
          Dashboard              Security Reports
                                  /          \
                                 v            v
                              JSON           CSV
```

## Deployment

RDRS can run as a local security monitoring service using Uvicorn and a user-level systemd service.

```text
RDRS Application
      |
      v
Uvicorn
      |
      v
FastAPI Application
      |
      v
RDRS Security Monitoring Service
      |
      v
Configured Monitoring Paths
```

## Technology Stack

- Python
- FastAPI
- SQLAlchemy
- SQLite
- Pydantic
- Watchdog
- psutil
- PyYAML
- Uvicorn
- Jinja2
- ReportLab
- Pytest
