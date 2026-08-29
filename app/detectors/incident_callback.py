from datetime import datetime
from hashlib import sha256

from app.database.incident_models import Evidence, Incident
from app.database.repository import EventRepository
from app.database.session import get_session
from app.detectors.base import FileEvent
from app.detectors.engine import DetectionResult


def _file_sha256(path) -> str | None:
    try:
        digest = sha256()
        with path.open("rb") as file:
            for chunk in iter(lambda: file.read(1024 * 1024), b""):
                digest.update(chunk)
        return digest.hexdigest()
    except (OSError, PermissionError):
        return None


def persist_detection(
    event: FileEvent,
    result: DetectionResult,
) -> None:
    session = get_session()

    try:
        event_repo = EventRepository(session)

        entropy = getattr(result, "entropy", None)
        suspicious = bool(
            getattr(result, "suspicious", False)
            or getattr(result, "is_suspicious", False)
        )

        event_repo.add(
            event_type=event.event_type,
            path=str(event.path),
            extension=event.path.suffix,
            timestamp=datetime.utcnow(),
            entropy=entropy,
            suspicious=suspicious,
        )

        if not suspicious:
            return

        incident = Incident(
            incident_id=f"INC-{datetime.utcnow().strftime('%Y%m%d%H%M%S%f')}",
            severity="high",
            threat_score=min(
                100.0,
                float(entropy or 0.0) * 10.0,
            ),
            status="open",
            summary=f"Suspicious activity detected: {event.path}",
        )

        session.add(incident)
        session.flush()

        evidence = Evidence(
            incident_id=incident.id,
            path=str(event.path),
            evidence_type="file",
            sha256=_file_sha256(event.path),
        )

        session.add(evidence)
        session.commit()

    except Exception:
        session.rollback()
        raise
    finally:
        session.close()
