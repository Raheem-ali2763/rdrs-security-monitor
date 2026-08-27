from datetime import datetime
from pathlib import Path

from app.detectors.base import FileEvent


def test_file_event_create_normalizes_path_and_extension():
    event = FileEvent.create(
        event_type="modify",
        path="data/sandbox/document.DOCX",
    )

    assert event.event_type == "modify"
    assert event.path == Path("data/sandbox/document.DOCX")
    assert event.extension == ".docx"
    assert isinstance(event.timestamp, datetime)


def test_file_event_uses_provided_timestamp():
    timestamp = datetime(2026, 8, 27, 15, 0, 0)

    event = FileEvent.create(
        event_type="rename",
        path="data/sandbox/file.locked",
        timestamp=timestamp,
    )

    assert event.event_type == "rename"
    assert event.timestamp == timestamp
    assert event.extension == ".locked"
