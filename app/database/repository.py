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


from app.database.models import ProcessSnapshot


class ProcessRepository:
    """Repository for storing and retrieving process telemetry snapshots."""

    def __init__(self, session: Session) -> None:
        self.session = session

    def add(
        self,
        *,
        pid: int,
        name: str,
        cpu_percent: float = 0.0,
        memory_percent: float = 0.0,
        disk_write_bytes: int = 0,
        executable: str | None = None,
        parent_pid: int | None = None,
        parent_name: str | None = None,
        unknown_process: bool = False,
        timestamp: datetime | None = None,
    ) -> ProcessSnapshot:
        """Create and persist a process telemetry snapshot."""
        snapshot = ProcessSnapshot(
            pid=pid,
            name=name,
            cpu_percent=cpu_percent,
            memory_percent=memory_percent,
            disk_write_bytes=disk_write_bytes,
            executable=executable,
            parent_pid=parent_pid,
            parent_name=parent_name,
            unknown_process=unknown_process,
            timestamp=timestamp or datetime.utcnow(),
        )

        self.session.add(snapshot)
        self.session.commit()
        self.session.refresh(snapshot)

        return snapshot

    def list_recent(self, limit: int = 100) -> Sequence[ProcessSnapshot]:
        """Return the most recent process snapshots."""
        statement = (
            select(ProcessSnapshot)
            .order_by(ProcessSnapshot.timestamp.desc())
            .limit(limit)
        )

        return self.session.scalars(statement).all()

    def count(self) -> int:
        """Return the total number of process snapshots."""
        statement = select(ProcessSnapshot)
        return len(self.session.scalars(statement).all())
