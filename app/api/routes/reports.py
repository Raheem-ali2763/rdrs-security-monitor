from fastapi import APIRouter
from app.database.incident_models import Incident
from app.database.models import Event
from app.database.session import get_session

router = APIRouter(prefix="/api", tags=["reports"])


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
