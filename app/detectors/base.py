from dataclasses import dataclass
from datetime import datetime
from pathlib import Path


@dataclass(frozen=True, slots=True)
class FileEvent:
    """Normalized file-system event used by RDRS."""

    event_type: str
    path: Path
    timestamp: datetime
    extension: str

    @classmethod
    def create(
        cls,
        event_type: str,
        path: str | Path,
        timestamp: datetime | None = None,
    ) -> "FileEvent":
        """Create a normalized file event."""
        file_path = Path(path)

        return cls(
            event_type=event_type,
            path=file_path,
            timestamp=timestamp or datetime.now(),
            extension=file_path.suffix.lower(),
        )
