from datetime import datetime

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from app.database.incident_models import Evidence, Incident
from app.database.session import get_session


router = APIRouter(prefix="/api", tags=["incidents"])


class IncidentCreate(BaseModel):
    incident_id: str
    severity: str = "normal"
    threat_score: float = 0.0
    summary: str = ""


class EvidenceCreate(BaseModel):
    path: str
    evidence_type: str = "file"
    sha256: str | None = None


def incident_dict(incident: Incident) -> dict:
    return {
        "id": incident.id,
        "incident_id": incident.incident_id,
        "severity": incident.severity,
        "threat_score": incident.threat_score,
        "status": incident.status,
        "summary": incident.summary,
        "started_at": incident.started_at.isoformat(),
        "ended_at": incident.ended_at.isoformat() if incident.ended_at else None,
    }


def evidence_dict(evidence: Evidence) -> dict:
    return {
        "id": evidence.id,
        "incident_id": evidence.incident_id,
        "path": evidence.path,
        "evidence_type": evidence.evidence_type,
        "sha256": evidence.sha256,
        "collected_at": evidence.collected_at.isoformat(),
    }


@router.get("/incidents")
def list_incidents() -> list[dict]:
    session = get_session()
    try:
        incidents = (
            session.query(Incident)
            .order_by(Incident.started_at.desc())
            .all()
        )
        return [incident_dict(i) for i in incidents]
    finally:
        session.close()


@router.post("/incidents", status_code=201)
def create_incident(payload: IncidentCreate) -> dict:
    session = get_session()
    try:
        existing = (
            session.query(Incident)
            .filter(Incident.incident_id == payload.incident_id)
            .first()
        )

        if existing:
            raise HTTPException(
                status_code=409,
                detail="Incident already exists",
            )

        incident = Incident(
            incident_id=payload.incident_id,
            severity=payload.severity,
            threat_score=payload.threat_score,
            summary=payload.summary,
        )

        session.add(incident)
        session.commit()
        session.refresh(incident)

        return incident_dict(incident)
    finally:
        session.close()


@router.get("/incidents/{incident_id}")
def get_incident(incident_id: int) -> dict:
    session = get_session()
    try:
        incident = session.get(Incident, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        return incident_dict(incident)
    finally:
        session.close()


@router.post("/incidents/{incident_id}/evidence", status_code=201)
def add_evidence(
    incident_id: int,
    payload: EvidenceCreate,
) -> dict:
    session = get_session()
    try:
        incident = session.get(Incident, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        evidence = Evidence(
            incident_id=incident.id,
            path=payload.path,
            evidence_type=payload.evidence_type,
            sha256=payload.sha256,
        )

        session.add(evidence)
        session.commit()
        session.refresh(evidence)

        return evidence_dict(evidence)
    finally:
        session.close()


@router.get("/incidents/{incident_id}/evidence")
def list_evidence(incident_id: int) -> list[dict]:
    session = get_session()
    try:
        incident = session.get(Incident, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        return [evidence_dict(e) for e in incident.evidence]
    finally:
        session.close()
