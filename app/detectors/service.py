from app.database.incident_models import Evidence, Incident
from app.database.models import Event
from app.database.session import get_session
from app.detectors.base import FileEvent
from app.detectors.file_monitor import FileMonitor
from app.detectors.pipeline import DetectionPipeline


class RDRSService:
    """Run the RDRS file-monitoring, detection, and persistence pipeline."""

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
        session = get_session()

        try:
            db_event = Event(
                event_type=event.event_type,
                path=str(event.path),
                extension=event.path.suffix,
                entropy=result.entropy,
                suspicious=result.suspicious,
            )

            session.add(db_event)
            session.commit()

            if result.suspicious:
                incident = Incident(
                    incident_id=f"INC-{db_event.id:04d}",
                    severity="critical",
                    threat_score=min(100.0, result.entropy * 10),
                    summary=f"Suspicious activity detected: {event.path}",
                )

                session.add(incident)
                session.flush()

                evidence = Evidence(
                    incident_id=incident.id,
                    path=str(event.path),
                    evidence_type="file",
                )

                session.add(evidence)
                session.commit()

            print(
                f"[RDRS] {event.event_type.upper():<7} "
                f"{event.path} | "
                f"entropy={result.entropy:.2f} | "
                f"suspicious={result.suspicious} | "
                f"signals={result.signals}"
            )

        finally:
            session.close()

    def start(self) -> None:
        self.monitor.start()

    def stop(self) -> None:
        self.monitor.stop()
