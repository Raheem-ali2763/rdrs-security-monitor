from datetime import datetime

from fastapi import APIRouter, HTTPException
from app.database.incident_models import Incident
from app.database.session import get_session


router = APIRouter(prefix="/api", tags=["response"])


@router.post("/incidents/{incident_id}/resolve")
def resolve_incident(incident_id: int) -> dict:
    session = get_session()

    try:
        incident = session.get(Incident, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        incident.status = "resolved"
        incident.ended_at = datetime.utcnow()

        session.commit()
        session.refresh(incident)

        return {
            "id": incident.id,
            "incident_id": incident.incident_id,
            "status": incident.status,
            "ended_at": incident.ended_at.isoformat(),
        }
    finally:
        session.close()


@router.post("/incidents/{incident_id}/reopen")
def reopen_incident(incident_id: int) -> dict:
    session = get_session()

    try:
        incident = session.get(Incident, incident_id)

        if incident is None:
            raise HTTPException(
                status_code=404,
                detail="Incident not found",
            )

        incident.status = "open"
        incident.ended_at = None

        session.commit()
        session.refresh(incident)

        return {
            "id": incident.id,
            "incident_id": incident.incident_id,
            "status": incident.status,
            "ended_at": None,
        }
    finally:
        session.close()
