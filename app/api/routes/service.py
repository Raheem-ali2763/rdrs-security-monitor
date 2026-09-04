from fastapi import APIRouter

from app.core.config import config
from app.database.repository import ProcessRepository
from app.database.session import get_session
from app.detectors.service import RDRSService


router = APIRouter(
    prefix="/api/service",
    tags=["service"],
)

_service: RDRSService | None = None


def _create_service() -> RDRSService:
    monitoring = config.get("monitoring", {})

    paths = monitoring.get(
        "paths",
        ["./data/sandbox"],
    )

    return RDRSService(paths=paths)


@router.post("/start")
def start_service() -> dict[str, str]:
    global _service

    if _service is not None:
        return {"status": "already_running"}

    _service = _create_service()
    _service.start()

    return {"status": "started"}


@router.post("/stop")
def stop_service() -> dict[str, str]:
    global _service

    if _service is None:
        return {"status": "already_stopped"}

    _service.stop()
    _service = None

    return {"status": "stopped"}


@router.get("/status")
def service_status() -> dict:
    activity = None

    if _service is not None:
        snapshot = _service.pipeline.snapshot()

        activity = {
            "window_seconds": snapshot.window_seconds,
            "event_count": snapshot.event_count,
            "modified_files": snapshot.modified_files,
            "renames": snapshot.renames,
            "extension_changes": snapshot.extension_changes,
            "average_entropy": snapshot.average_entropy,
            "rapid_activity": snapshot.rapid_activity,
            "mass_rename": snapshot.mass_rename,
            "high_entropy": snapshot.high_entropy,
        }

    session = get_session()

    try:
        process_count = ProcessRepository(session).count()
    finally:
        session.close()

    return {
        "running": _service is not None,
        "activity": activity,
        "process_snapshots": process_count,
    }
