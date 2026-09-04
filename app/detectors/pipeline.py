from collections.abc import Callable

import psutil

from app.detectors.activity_window import ActivitySnapshot, ActivityWindow
from app.detectors.base import FileEvent
from app.detectors.engine import DetectionEngine, DetectionResult
from app.detectors.incident_callback import persist_detection
from app.detectors.process_telemetry import ProcessTelemetry


class DetectionPipeline:
    """Connect filesystem events to the RDRS detection and scoring engine."""

    def __init__(
        self,
        engine: DetectionEngine | None = None,
        callback: Callable[[FileEvent, DetectionResult], None] | None = None,
        activity_window: ActivityWindow | None = None,
        process_telemetry: ProcessTelemetry | None = None,
    ) -> None:
        self.engine = engine or DetectionEngine()
        self.callback = callback or persist_detection
        self.activity_window = activity_window or ActivityWindow()
        self.process_telemetry = process_telemetry or ProcessTelemetry()

        self.last_snapshot: ActivitySnapshot | None = None

    def _process_signals(self) -> tuple[bool, bool]:
        """Return CPU-spike and unknown-process signals from current processes."""
        cpu_spike = False
        unknown_process = False

        for process in psutil.process_iter(["pid", "name"]):
            try:
                snapshot = self.process_telemetry.snapshot(process)

                if self.process_telemetry.is_cpu_spike(snapshot):
                    cpu_spike = True

                if snapshot.unknown_process:
                    unknown_process = True

                if cpu_spike and unknown_process:
                    break

            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue

        return cpu_spike, unknown_process

    def process(self, event: FileEvent) -> DetectionResult | None:
        """Process a filesystem event through the rolling detection pipeline."""

        entropy = None

        if event.path.is_file():
            try:
                result = self.engine.analyze(event.path)
                entropy = result.entropy
            except (OSError, PermissionError):
                result = None
        else:
            result = None

        snapshot = self.activity_window.add(
            event,
            entropy=entropy,
        )

        self.last_snapshot = snapshot

        if not event.path.is_file():
            return None

        cpu_spike, unknown_process = self._process_signals()

        result = self.engine.analyze(
            event.path,
            rapid_file_modification=snapshot.rapid_activity,
            mass_rename=snapshot.mass_rename,
            cpu_spike=cpu_spike,
            unknown_process=unknown_process,
        )

        if self.callback is not None:
            self.callback(event, result)

        return result

    def snapshot(self) -> ActivitySnapshot:
        """Return the current rolling activity snapshot."""
        snapshot = self.activity_window.snapshot()
        self.last_snapshot = snapshot
        return snapshot
