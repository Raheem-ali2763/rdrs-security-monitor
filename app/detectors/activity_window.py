from __future__ import annotations

from collections import deque
from dataclasses import dataclass
from datetime import datetime, timedelta
from pathlib import Path

from app.core.config import config
from app.detectors.base import FileEvent


@dataclass(frozen=True, slots=True)
class ActivitySnapshot:
    window_seconds: int
    event_count: int
    modified_files: int
    renames: int
    extension_changes: int
    average_entropy: float
    rapid_activity: bool
    mass_rename: bool
    high_entropy: bool


class ActivityWindow:
    """Track file activity inside a rolling configured time window."""

    def __init__(
        self,
        window_seconds: int | None = None,
        modified_files_threshold: int | None = None,
        rename_threshold: int | None = None,
        entropy_threshold: float | None = None,
    ) -> None:
        detection_config = config.get("detection", {})
        file_activity = detection_config.get("file_activity", {})
        entropy_config = detection_config.get("entropy", {})

        self.window_seconds = int(
            window_seconds
            if window_seconds is not None
            else file_activity.get("burst_window_seconds", 60)
        )

        self.modified_files_threshold = int(
            modified_files_threshold
            if modified_files_threshold is not None
            else file_activity.get("modified_files_threshold", 50)
        )

        self.rename_threshold = int(
            rename_threshold
            if rename_threshold is not None
            else file_activity.get("rename_threshold", 20)
        )

        self.entropy_threshold = float(
            entropy_threshold
            if entropy_threshold is not None
            else entropy_config.get("threshold", 7.5)
        )

        self.window = timedelta(seconds=self.window_seconds)
        self.events: deque[
            tuple[datetime, FileEvent, float | None]
        ] = deque()

    def add(
        self,
        event: FileEvent,
        entropy: float | None = None,
    ) -> ActivitySnapshot:
        now = datetime.utcnow()

        self.events.append((now, event, entropy))
        self._expire(now)

        modified_files = sum(
            1
            for _, item, _ in self.events
            if item.event_type == "modify"
        )

        renames = sum(
            1
            for _, item, _ in self.events
            if item.event_type == "rename"
        )

        extension_changes = self._count_extension_changes()

        entropy_values = [
            value
            for _, _, value in self.events
            if value is not None
        ]

        average_entropy = (
            sum(entropy_values) / len(entropy_values)
            if entropy_values
            else 0.0
        )

        return ActivitySnapshot(
            window_seconds=self.window_seconds,
            event_count=len(self.events),
            modified_files=modified_files,
            renames=renames,
            extension_changes=extension_changes,
            average_entropy=round(average_entropy, 4),
            rapid_activity=(
                modified_files >= self.modified_files_threshold
            ),
            mass_rename=(
                renames >= self.rename_threshold
            ),
            high_entropy=(
                average_entropy >= self.entropy_threshold
            ),
        )

    def _expire(self, now: datetime) -> None:
        cutoff = now - self.window

        while self.events and self.events[0][0] < cutoff:
            self.events.popleft()

    def _count_extension_changes(self) -> int:
        paths: dict[str, str] = {}
        changes = 0

        for _, event, _ in self.events:
            path = str(event.path)
            extension = Path(path).suffix.lower()

            previous = paths.get(path)

            if previous is not None and previous != extension:
                changes += 1

            paths[path] = extension

        return changes

    def snapshot(self) -> ActivitySnapshot:
        """Return the current rolling-window state."""
        now = datetime.utcnow()
        self._expire(now)

        modified_files = sum(
            1
            for _, item, _ in self.events
            if item.event_type == "modify"
        )

        renames = sum(
            1
            for _, item, _ in self.events
            if item.event_type == "rename"
        )

        extension_changes = self._count_extension_changes()

        entropy_values = [
            value
            for _, _, value in self.events
            if value is not None
        ]

        average_entropy = (
            sum(entropy_values) / len(entropy_values)
            if entropy_values
            else 0.0
        )

        return ActivitySnapshot(
            window_seconds=self.window_seconds,
            event_count=len(self.events),
            modified_files=modified_files,
            renames=renames,
            extension_changes=extension_changes,
            average_entropy=round(average_entropy, 4),
            rapid_activity=(
                modified_files >= self.modified_files_threshold
            ),
            mass_rename=(
                renames >= self.rename_threshold
            ),
            high_entropy=(
                average_entropy >= self.entropy_threshold
            ),
        )
