from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional


@dataclass
class ScanResult:
    scan_id: str
    filename: str
    path: str
    size: int
    extension: str
    mime_type: str
    sha256: str
    entropy: float
    indicators: list[str] = field(default_factory=list)
    score: int = 0
    severity: str = "Normal"
    verdict: str = "No Strong Indicators"
    quarantined: bool = False
    quarantine_path: Optional[str] = None

    def to_dict(self) -> dict:
        return {
            "scan_id": self.scan_id,
            "filename": self.filename,
            "path": self.path,
            "size": self.size,
            "extension": self.extension,
            "mime_type": self.mime_type,
            "sha256": self.sha256,
            "entropy": self.entropy,
            "indicators": self.indicators,
            "score": self.score,
            "severity": self.severity,
            "verdict": self.verdict,
            "quarantined": self.quarantined,
            "quarantine_path": self.quarantine_path,
        }
