from collections.abc import Sequence
from datetime import datetime

from sqlalchemy import select
from sqlalchemy.orm import Session

from app.database.models import Event


class EventRepository:
    """Repository for storing and retrieving RDRS filesystem events."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self,
        *,
        event_type: str,
        path: str,
        extension: str = "",
        timestamp: datetime | None = None,
        entropy: float | None = None,
        suspicious: bool = False,
    ) -> Event:
        """Create and persist a filesystem event."""
        event = Event(
            event_type=event_type,
            path=path,
            extension=extension,
            timestamp=timestamp or datetime.utcnow(),
            entropy=entropy,
            suspicious=suspicious,
        )

        self.session.add(event)
        self.session.commit()
        self.session.refresh(event)

        return event

    def get_by_id(self, event_id: int) -> Event | None:
        """Return one event by ID."""
        return self.session.get(Event, event_id)

    def list_recent(self, limit: int = 100) -> Sequence[Event]:
        """Return the most recent events."""
        statement = (
            select(Event)
            .order_by(Event.timestamp.desc())
            .limit(limit)
        )

        return self.session.scalars(statement).all()

    def count(self) -> int:
        """Return the total number of stored events."""
        statement = select(Event)
        return len(self.session.scalars(statement).all())
