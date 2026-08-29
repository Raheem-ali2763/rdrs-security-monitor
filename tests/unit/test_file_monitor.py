from pathlib import Path

from app.detectors.base import FileEvent
from app.detectors.file_monitor import RDRSEventHandler


def test_handler_converts_created_file_event():
    received_events: list[FileEvent] = []

    handler = RDRSEventHandler(received_events.append)

    class MockEvent:
        is_directory = False
        src_path = "data/sandbox/test.txt"

    handler.on_created(MockEvent())

    assert len(received_events) == 1

    event = received_events[0]

    assert event.event_type == "create"
    assert event.path == Path("data/sandbox/test.txt")
    assert event.extension == ".txt"


def test_handler_ignores_directory_events():
    received_events: list[FileEvent] = []

    handler = RDRSEventHandler(received_events.append)

    class MockEvent:
        is_directory = True
        src_path = "data/sandbox/test-dir"

    handler.on_created(MockEvent())

    assert received_events == []
