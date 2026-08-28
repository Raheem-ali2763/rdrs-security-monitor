from app.database.repository import EventRepository
from app.database.incident_models import Incident
from app.database.session import get_session
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
                existing = (
                    session.query(Incident)
                    .filter(
                        Incident.status == "open",
                        Incident.summary.contains(str(event.path)),
                    )
                    .first()
                )

                if existing is None:
                    next_id = session.query(Incident).count() + 1

                    incident = Incident(
                        incident_id=f"INC-{next_id:04d}",
                        severity="critical",
                        threat_score=min(100.0, result.entropy * 10.0),
                        summary=(
                            f"Suspicious activity detected: "
                            f"{event.path}"
                        ),
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
                        f"{existing.incident_id} | "
                        f"{event.path}"
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
