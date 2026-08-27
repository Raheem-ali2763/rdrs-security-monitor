from app.detectors.entropy_detector import EntropyDetector


def test_low_entropy_file_is_not_suspicious(tmp_path):
    path = tmp_path / "normal.txt"
    path.write_bytes(b"A" * 1000)

    result = EntropyDetector(threshold=7.0).analyze(path)

    assert result["entropy"] == 0.0
    assert result["suspicious"] is False


def test_high_entropy_file_is_suspicious(tmp_path):
    path = tmp_path / "random.bin"
    path.write_bytes(bytes(range(256)) * 10)

    result = EntropyDetector(threshold=7.0).analyze(path)

    assert result["entropy"] == 8.0
    assert result["suspicious"] is True


def test_missing_file_returns_error(tmp_path):
    path = tmp_path / "missing.bin"

    result = EntropyDetector().analyze(path)

    assert result["suspicious"] is False
    assert result["error"] == "file_not_found"
