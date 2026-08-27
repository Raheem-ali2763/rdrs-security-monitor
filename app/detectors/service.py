from app.detectors.base import FileEvent
from app.detectors.file_monitor import FileMonitor
from app.detectors.pipeline import DetectionPipeline


class RDRSService:
    """Run the RDRS file-monitoring and detection pipeline."""

    def __init__(self, paths: list[str]) -> None:
        self.pipeline = DetectionPipeline(
            callback=self._handle_detection,
        )
        self.monitor = FileMonitor(
            paths=paths,
            callback=self._handle_event,
        )

    def _handle_event(self, event: FileEvent) -> None:
        self.pipeline.process(event)

    @staticmethod
    def _handle_detection(event: FileEvent, result) -> None:
        print(
            f"[RDRS] {event.event_type.upper():<7} "
            f"{event.path} | "
            f"entropy={result.entropy:.2f} | "
            f"suspicious={result.suspicious} | "
            f"signals={result.signals}"
        )

    def start(self) -> None:
        """Start the RDRS monitoring service."""
        self.monitor.start()

    def stop(self) -> None:
        """Stop the RDRS monitoring service."""
        self.monitor.stop()
