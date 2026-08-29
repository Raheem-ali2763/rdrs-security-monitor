from collections.abc import Callable
from pathlib import Path

from app.detectors.base import FileEvent
from app.detectors.engine import DetectionEngine, DetectionResult
from app.detectors.incident_callback import persist_detection


class DetectionPipeline:
    """Connect filesystem events to the RDRS detection engine."""

    def __init__(
        self,
        engine: DetectionEngine | None = None,
        callback: Callable[[FileEvent, DetectionResult], None] | None = None,
    ) -> None:
        self.engine = engine or DetectionEngine()
        self.callback = callback or persist_detection

    def process(self, event: FileEvent) -> DetectionResult | None:
        """Process a filesystem event through the detection engine."""

        if event.event_type not in {"create", "modify"}:
            return None

        if not event.path.is_file():
            return None

        result = self.engine.analyze(event.path)

        if self.callback is not None:
            self.callback(event, result)

        return result
