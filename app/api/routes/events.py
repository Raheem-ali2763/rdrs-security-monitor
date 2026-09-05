from fastapi import APIRouter, HTTPException

from app.database.repository import EventRepository
from app.database.session import get_session


router = APIRouter(prefix="/api", tags=["events"])


def _event_to_dict(event) -> dict:
    return {
        "id": event.id,
        "event_type": event.event_type,
        "path": event.path,
        "extension": event.extension,
        "timestamp": event.timestamp.isoformat(),
        "entropy": event.entropy,
        "suspicious": event.suspicious,
    }


@router.get("/events")
def list_events(limit: int = 50) -> list[dict]:
    limit = max(1, min(limit, 200))

    session = get_session()
    try:
        repository = EventRepository(session)
        events = repository.list_recent(limit)
        return [_event_to_dict(event) for event in events]
    finally:
        session.close()


@router.get("/events/{event_id}")
def get_event(event_id: int) -> dict:
    session = get_session()
    try:
        repository = EventRepository(session)
        event = repository.get_by_id(event_id)

        if event is None:
            raise HTTPException(status_code=404, detail="Event not found")

        return _event_to_dict(event)
    finally:
        session.close()


@router.get("/stats")
def get_stats() -> dict:
    """Return live dashboard statistics from the database."""
    from datetime import datetime, timedelta

    from app.database.incident_models import Incident

    session = get_session()
    try:
        now = datetime.utcnow()
        today_start = datetime(now.year, now.month, now.day)
        recent_start = now - timedelta(minutes=5)

        total_events = session.query(EventRepository).count() if False else 0

        from app.database.models import Event

        total_events = session.query(Event).count()

        events_today = (
            session.query(Event)
            .filter(Event.timestamp >= today_start)
            .count()
        )

        suspicious_events = (
            session.query(Event)
            .filter(Event.suspicious.is_(True))
            .count()
        )

        recent_events = (
            session.query(Event)
            .filter(Event.timestamp >= recent_start)
            .count()
        )

        incidents = session.query(Incident).all()

        active_incidents = [
            incident
            for incident in incidents
            if str(incident.status).lower() == "open"
        ]

        resolved_incidents = [
            incident
            for incident in incidents
            if str(incident.status).lower() in {"resolved", "closed"}
        ]

        threat_score = 0.0

        if active_incidents:
            threat_score = max(
                float(incident.threat_score or 0)
                for incident in active_incidents
            )

        threat_score = round(max(0.0, min(100.0, threat_score)), 1)

        if threat_score >= 70:
            threat_label = "Elevated activity"
        elif threat_score >= 40:
            threat_label = "Moderate activity"
        elif threat_score > 0:
            threat_label = "Low activity"
        else:
            threat_label = "No active threat"

        return {
            "total_events": total_events,
            "events_today": events_today,
            "suspicious_events": suspicious_events,
            "recent_events": recent_events,
            "active_incidents": len(active_incidents),
            "total_incidents": len(incidents),
            "resolved_incidents": len(resolved_incidents),
            "threat_score": threat_score,
            "threat_label": threat_label,
        }
    finally:
        session.close()

