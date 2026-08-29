from datetime import datetime

from sqlalchemy import create_engine
from sqlalchemy.orm import Session

from app.database.models import Base
from app.database.repository import EventRepository


def create_test_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_repository_adds_and_reads_event():
    session = create_test_session()

    try:
        repository = EventRepository(session)

        timestamp = datetime(2026, 8, 27, 15, 30, 0)

        event = repository.add(
            event_type="modify",
            path="data/sandbox/example.bin",
            extension=".bin",
            timestamp=timestamp,
            entropy=8.0,
            suspicious=True,
        )

        assert event.id is not None
        assert event.event_type == "modify"
        assert event.path == "data/sandbox/example.bin"
        assert event.extension == ".bin"
        assert event.entropy == 8.0
        assert event.suspicious is True

        stored = repository.get_by_id(event.id)

        assert stored is not None
        assert stored.id == event.id
        assert stored.path == event.path
    finally:
        session.close()


def test_repository_lists_recent_events():
    session = create_test_session()

    try:
        repository = EventRepository(session)

        repository.add(
            event_type="create",
            path="data/sandbox/first.txt",
            timestamp=datetime(2026, 8, 27, 15, 0, 0),
        )

        repository.add(
            event_type="modify",
            path="data/sandbox/second.txt",
            timestamp=datetime(2026, 8, 27, 15, 5, 0),
        )

        events = repository.list_recent(limit=10)

        assert len(events) == 2
        assert events[0].path == "data/sandbox/second.txt"
        assert events[1].path == "data/sandbox/first.txt"
    finally:
        session.close()


def test_repository_counts_events():
    session = create_test_session()

    try:
        repository = EventRepository(session)

        assert repository.count() == 0

        repository.add(
            event_type="create",
            path="data/sandbox/example.txt",
        )

        repository.add(
            event_type="modify",
            path="data/sandbox/example.txt",
        )

        assert repository.count() == 2
    finally:
        session.close()
