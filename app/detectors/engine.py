from dataclasses import dataclass, field
from pathlib import Path

from app.detectors.entropy_detector import EntropyDetector


@dataclass(frozen=True, slots=True)
class DetectionResult:
    path: Path
    entropy: float
    suspicious: bool
    signals: list[str] = field(default_factory=list)


class DetectionEngine:
    """Coordinate RDRS detectors and produce a unified result."""

    def __init__(self, entropy_threshold: float = 7.0) -> None:
        self.entropy_detector = EntropyDetector(
            threshold=entropy_threshold
        )

    def analyze(self, path: str | Path) -> DetectionResult:
        result = self.entropy_detector.analyze(path)

        signals: list[str] = []

        if result["suspicious"]:
            signals.append("high_entropy")

        return DetectionResult(
            path=Path(result["path"]),
            entropy=result["entropy"],
            suspicious=result["suspicious"],
            signals=signals,
        )
