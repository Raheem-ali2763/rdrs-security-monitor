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
    session = get_session()
    try:
        repository = EventRepository(session)
        events = repository.list_recent(200)

        suspicious = sum(1 for event in events if event.suspicious)

        return {
            "total_events": repository.count(),
            "recent_events": len(events),
            "suspicious_events": suspicious,
        }
    finally:
        session.close()
