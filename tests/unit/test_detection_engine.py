from pathlib import Path

from app.detectors.engine import DetectionEngine


def test_detection_engine_marks_high_entropy_file_suspicious(tmp_path):
    path = tmp_path / "suspicious.bin"
    path.write_bytes(bytes(range(256)) * 10)

    result = DetectionEngine(entropy_threshold=7.0).analyze(path)

    assert result.path == path
    assert result.entropy == 8.0
    assert result.suspicious is True
    assert "high_entropy" in result.signals


def test_detection_engine_marks_low_entropy_file_normal(tmp_path):
    path = tmp_path / "normal.txt"
    path.write_bytes(b"A" * 1000)

    result = DetectionEngine(entropy_threshold=7.0).analyze(path)

    assert result.path == path
    assert result.entropy == 0.0
    assert result.suspicious is False
    assert result.signals == []
