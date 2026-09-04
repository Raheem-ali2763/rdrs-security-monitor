from dataclasses import dataclass, field
from pathlib import Path

from app.core.config import config
from app.detectors.entropy_detector import EntropyDetector


@dataclass(frozen=True, slots=True)
class DetectionResult:
    path: Path
    entropy: float
    suspicious: bool
    signals: list[str] = field(default_factory=list)
    score: float = 0.0
    severity: str = "Normal"


class DetectionEngine:
    """Coordinate RDRS detectors using configuration-driven scoring."""

    def __init__(
        self,
        entropy_threshold: float | None = None,
    ) -> None:
        detection_config = config.get("detection", {})
        scoring_config = config.get("scoring", {})

        weights = scoring_config.get("weights", {})
        levels = scoring_config.get("levels", {})

        self.RAPID_FILE_MODIFICATION = float(
            weights.get("rapid_file_modification", 40)
        )
        self.MASS_RENAME = float(
            weights.get("mass_rename", 30)
        )
        self.HIGH_ENTROPY = float(
            weights.get("high_entropy", 25)
        )
        self.CPU_SPIKE = float(
            weights.get("cpu_spike", 15)
        )
        self.UNKNOWN_PROCESS = float(
            weights.get("unknown_process", 10)
        )

        self.NORMAL_MAX = float(
            levels.get("normal_max", 40)
        )
        self.WARNING_MAX = float(
            levels.get("warning_max", 70)
        )
        self.CRITICAL_MAX = float(
            levels.get("critical_max", 100)
        )

        entropy_config = detection_config.get("entropy", {})

        threshold = (
            entropy_threshold
            if entropy_threshold is not None
            else float(entropy_config.get("threshold", 7.5))
        )

        self.entropy_detector = EntropyDetector(
            threshold=threshold
        )

    def severity_for_score(self, score: float) -> str:
        """Map a score to the configured RDRS severity level."""
        if score >= self.WARNING_MAX:
            return "Critical"

        if score >= self.NORMAL_MAX:
            return "Warning"

        return "Normal"

    def analyze(
        self,
        path: str | Path,
        *,
        rapid_file_modification: bool = False,
        mass_rename: bool = False,
        cpu_spike: bool = False,
        unknown_process: bool = False,
    ) -> DetectionResult:
        """Analyze a file and calculate its weighted threat score."""
        result = self.entropy_detector.analyze(path)

        signals: list[str] = []
        score = 0.0

        if result["suspicious"]:
            signals.append("high_entropy")
            score += self.HIGH_ENTROPY

        if rapid_file_modification:
            signals.append("rapid_file_modification")
            score += self.RAPID_FILE_MODIFICATION

        if mass_rename:
            signals.append("mass_rename")
            score += self.MASS_RENAME

        if cpu_spike:
            signals.append("cpu_spike")
            score += self.CPU_SPIKE

        if unknown_process:
            signals.append("unknown_process")
            score += self.UNKNOWN_PROCESS

        score = min(score, self.CRITICAL_MAX)

        return DetectionResult(
            path=Path(result["path"]),
            entropy=result["entropy"],
            suspicious=bool(
                result["suspicious"] or score >= self.NORMAL_MAX
            ),
            signals=signals,
            score=score,
            severity=self.severity_for_score(score),
        )
