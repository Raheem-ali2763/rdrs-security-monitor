from threading import Lock

from app.database.incident_models import Incident
from app.database.repository import EventRepository
from app.database.session import get_session
from app.detectors.base import FileEvent
from app.detectors.file_monitor import FileMonitor
from app.detectors.pipeline import DetectionPipeline


class RDRSService:
    """Run the RDRS file-monitoring and detection pipeline."""

    _incident_lock = Lock()

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

    @classmethod
    def _handle_detection(cls, event: FileEvent, result) -> None:
        session = get_session()

        try:
            repository = EventRepository(session)
            extension = event.path.suffix.lower()

            repository.add(
                event_type=event.event_type,
                path=str(event.path),
                extension=extension,
                entropy=result.entropy,
                suspicious=result.suspicious,
            )

            if result.suspicious:
                path = str(event.path)

                with cls._incident_lock:
                    existing = (
                        session.query(Incident)
                        .filter(
                            Incident.status == "open",
                            Incident.summary == (
                                f"Suspicious activity detected: {path}"
                            ),
                        )
                        .first()
                    )

                    if existing is None:
                        next_id = session.query(Incident).count() + 1

                        incident = Incident(
                            incident_id=f"INC-{next_id:04d}",
                            severity="critical",
                            threat_score=min(
                                100.0,
                                result.entropy * 10.0,
                            ),
                            summary=f"Suspicious activity detected: {path}",
                        )

                        session.add(incident)
                        session.commit()

                        print(
                            f"[RDRS] INCIDENT CREATED | "
                            f"{incident.incident_id} | "
                            f"score={incident.threat_score:.1f}"
                        )
                    else:
                        print(
                            f"[RDRS] INCIDENT EXISTS | "
                            f"{existing.incident_id} | {path}"
                        )

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
        """Start the RDRS monitoring service."""
        self.monitor.start()

    def stop(self) -> None:
        """Stop the RDRS monitoring service."""
        self.monitor.stop()
