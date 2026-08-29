from datetime import datetime

from app.database.models import Event


def test_event_model_contains_expected_columns():
    columns = Event.__table__.columns

    assert "id" in columns
    assert "event_type" in columns
    assert "path" in columns
    assert "extension" in columns
    assert "timestamp" in columns
    assert "entropy" in columns
    assert "suspicious" in columns


def test_event_model_has_expected_table_name():
    assert Event.__tablename__ == "events"


def test_event_model_accepts_event_data():
    event = Event(
        event_type="modify",
        path="data/sandbox/example.txt",
        extension=".txt",
        timestamp=datetime(2026, 8, 27, 15, 0, 0),
        entropy=2.5,
        suspicious=False,
    )

    assert event.event_type == "modify"
    assert event.path == "data/sandbox/example.txt"
    assert event.extension == ".txt"
    assert event.entropy == 2.5
    assert event.suspicious is False
