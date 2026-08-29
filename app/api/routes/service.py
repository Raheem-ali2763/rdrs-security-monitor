from fastapi import APIRouter

from app.detectors.service import RDRSService


router = APIRouter(prefix="/api/service", tags=["service"])

_service: RDRSService | None = None


@router.post("/start")
def start_service() -> dict[str, str]:
    global _service

    if _service is not None:
        return {"status": "already_running"}

    _service = RDRSService(["data/sandbox"])
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
def service_status() -> dict[str, bool]:
    return {
        "running": _service is not None,
    }
