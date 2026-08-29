from pathlib import Path

from app.detectors.base import FileEvent
from app.detectors.engine import DetectionResult
from app.detectors.pipeline import DetectionPipeline


def test_pipeline_processes_create_event(tmp_path):
    path = tmp_path / "suspicious.bin"
    path.write_bytes(bytes(range(256)) * 10)

    received = []

    def callback(event, result):
        received.append((event, result))

    pipeline = DetectionPipeline(callback=callback)

    event = FileEvent.create(
        event_type="create",
        path=path,
    )

    result = pipeline.process(event)

    assert isinstance(result, DetectionResult)
    assert result.path == path
    assert result.suspicious is True
    assert "high_entropy" in result.signals

    assert len(received) == 1
    assert received[0][0] == event
    assert received[0][1] == result


def test_pipeline_ignores_delete_event(tmp_path):
    path = tmp_path / "file.txt"
    path.write_text("normal file")

    received = []

    pipeline = DetectionPipeline(
        callback=lambda event, result: received.append((event, result))
    )

    event = FileEvent.create(
        event_type="delete",
        path=path,
    )

    result = pipeline.process(event)

    assert result is None
    assert received == []


def test_pipeline_ignores_missing_file(tmp_path):
    path = tmp_path / "missing.txt"

    pipeline = DetectionPipeline()

    event = FileEvent.create(
        event_type="modify",
        path=path,
    )

    result = pipeline.process(event)

    assert result is None
