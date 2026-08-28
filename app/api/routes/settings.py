from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter(prefix="/api", tags=["settings"])


class SettingsUpdate(BaseModel):
    monitoring_enabled: bool | None = None
    monitored_path: str | None = None
    entropy_threshold: float | None = None


_settings = {
    "monitoring_enabled": True,
    "monitored_path": "data/sandbox",
    "entropy_threshold": 7.0,
}


@router.get("/settings")
def get_settings() -> dict:
    return _settings.copy()


@router.patch("/settings")
def update_settings(payload: SettingsUpdate) -> dict:
    if payload.monitoring_enabled is not None:
        _settings["monitoring_enabled"] = payload.monitoring_enabled

    if payload.monitored_path is not None:
        _settings["monitored_path"] = payload.monitored_path

    if payload.entropy_threshold is not None:
        _settings["entropy_threshold"] = payload.entropy_threshold

    return _settings.copy()
