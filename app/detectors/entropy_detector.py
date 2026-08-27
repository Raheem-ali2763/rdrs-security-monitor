from pathlib import Path

from app.core.entropy import calculate_file_entropy


class EntropyDetector:
    def __init__(self, threshold: float = 7.0):
        self.threshold = threshold

    def analyze(self, path: str | Path) -> dict:
        path = Path(path)

        if not path.is_file():
            return {
                "path": str(path),
                "entropy": 0.0,
                "threshold": self.threshold,
                "suspicious": False,
                "error": "file_not_found",
            }

        entropy = calculate_file_entropy(path)

        return {
            "path": str(path),
            "entropy": entropy,
            "threshold": self.threshold,
            "suspicious": entropy >= self.threshold,
            "error": None,
        }
