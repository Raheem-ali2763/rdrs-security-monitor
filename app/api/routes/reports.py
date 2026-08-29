from datetime import datetime
from pathlib import Path
import csv
import io
import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import FileResponse

from app.database.incident_models import Incident
from app.database.models import Event
from app.database.session import get_session


router = APIRouter(prefix="/api", tags=["reports"])

REPORT_DIR = Path("data/reports")
REPORT_DIR.mkdir(parents=True, exist_ok=True)


def _incident_lookup(session, incident_ref: str):
    incident = None

    if incident_ref.isdigit():
        incident = session.get(Incident, int(incident_ref))

    if incident is None:
        incident = (
            session.query(Incident)
            .filter(Incident.incident_id == incident_ref)
            .first()
        )

    return incident


def _model_dict(obj) -> dict:
    if obj is None:
        return {}

    result = {}

    for column in obj.__table__.columns:
        value = getattr(obj, column.name, None)

        if isinstance(value, datetime):
            value = value.isoformat()

        result[column.name] = value

    return result


def _recommendations(incident: Incident) -> list[str]:
    recommendations = [
        "Review the affected files and associated evidence.",
        "Verify whether the activity was authorized.",
        "Preserve the collected evidence for investigation.",
    ]

    if float(incident.threat_score or 0) >= 70:
        recommendations.insert(
            0,
            "Treat this incident as critical and investigate immediately.",
        )

    if incident.status == "open":
        recommendations.append(
            "Incident remains open and should be reviewed or resolved."
        )

    return recommendations


def _build_report(session, incident: Incident) -> dict:
    evidence = list(incident.evidence or [])

    events = session.query(Event).all()

    event_rows = []
    suspect_processes = set()

    for event in events:
        row = _model_dict(event)

        # Keep only useful timeline information when possible.
        event_rows.append(row)

        for key in (
            "process",
            "process_name",
            "process_path",
            "executable",
            "source_process",
        ):
            value = row.get(key)
            if value:
                suspect_processes.add(str(value))

    affected_files = []
    evidence_rows = []

    for item in evidence:
        row = _model_dict(item)
        evidence_rows.append(row)

        if item.path:
            affected_files.append(item.path)

    timeline = [
        {
            "type": "incident_started",
            "timestamp": (
                incident.started_at.isoformat()
                if incident.started_at
                else None
            ),
            "description": incident.summary,
        }
    ]

    if incident.ended_at:
        timeline.append(
            {
                "type": "incident_ended",
                "timestamp": incident.ended_at.isoformat(),
                "description": f"Incident status: {incident.status}",
            }
        )

    return {
        "incident": _model_dict(incident),
        "timeline": timeline,
        "threat_score": float(incident.threat_score or 0),
        "severity": incident.severity,
        "status": incident.status,
        "summary": incident.summary,
        "affected_files": sorted(set(affected_files)),
        "suspect_processes": sorted(suspect_processes),
        "evidence": evidence_rows,
        "events": event_rows,
        "recommendations": _recommendations(incident),
        "generated_at": datetime.utcnow().isoformat(),
    }


@router.get("/reports/summary")
def report_summary() -> dict:
    session = get_session()

    try:
        incidents = session.query(Incident).all()
        events = session.query(Event).all()

        open_incidents = sum(
            1 for incident in incidents
            if incident.status == "open"
        )

        suspicious_events = sum(
            1 for event in events
            if event.suspicious
        )

        return {
            "total_events": len(events),
            "suspicious_events": suspicious_events,
            "total_incidents": len(incidents),
            "open_incidents": open_incidents,
            "resolved_incidents": sum(
                1 for incident in incidents
                if incident.status in {"resolved", "closed"}
            ),
        }

    finally:
        session.close()


@router.get("/reports/{incident_ref}/json")
def generate_json_report(incident_ref: str):
    session = get_session()

    try:
        incident = _incident_lookup(session, incident_ref)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        report = _build_report(session, incident)

        filename = f"{incident.incident_id}.json"
        path = REPORT_DIR / filename

        path.write_text(
            json.dumps(report, indent=2, default=str),
            encoding="utf-8",
        )

        return FileResponse(
            path=str(path),
            media_type="application/json",
            filename=filename,
        )

    finally:
        session.close()


@router.get("/reports/{incident_ref}/csv")
def generate_csv_report(incident_ref: str):
    session = get_session()

    try:
        incident = _incident_lookup(session, incident_ref)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        report = _build_report(session, incident)

        output = io.StringIO()
        writer = csv.writer(output)

        writer.writerow(["RDRS INCIDENT REPORT"])
        writer.writerow(["Incident ID", incident.incident_id])
        writer.writerow(["Severity", incident.severity])
        writer.writerow(["Threat Score", incident.threat_score])
        writer.writerow(["Status", incident.status])
        writer.writerow(["Summary", incident.summary])
        writer.writerow([])

        writer.writerow(["TIMELINE"])
        writer.writerow(["Type", "Timestamp", "Description"])

        for item in report["timeline"]:
            writer.writerow(
                [
                    item["type"],
                    item["timestamp"],
                    item["description"],
                ]
            )

        writer.writerow([])
        writer.writerow(["AFFECTED FILES"])

        for path in report["affected_files"]:
            writer.writerow([path])

        writer.writerow([])
        writer.writerow(["SUSPECT PROCESSES"])

        for process in report["suspect_processes"]:
            writer.writerow([process])

        writer.writerow([])
        writer.writerow(["EVIDENCE"])
        writer.writerow(
            ["ID", "Path", "Type", "SHA256", "Collected At"]
        )

        for item in report["evidence"]:
            writer.writerow(
                [
                    item.get("id"),
                    item.get("path"),
                    item.get("evidence_type"),
                    item.get("sha256"),
                    item.get("collected_at"),
                ]
            )

        writer.writerow([])
        writer.writerow(["RECOMMENDATIONS"])

        for recommendation in report["recommendations"]:
            writer.writerow([recommendation])

        filename = f"{incident.incident_id}.csv"
        path = REPORT_DIR / filename

        path.write_text(
            output.getvalue(),
            encoding="utf-8",
        )

        return FileResponse(
            path=str(path),
            media_type="text/csv",
            filename=filename,
        )

    finally:
        session.close()
