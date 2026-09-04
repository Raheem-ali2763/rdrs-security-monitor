import os
from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.events import router as events_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.response import router as response_router
from app.api.routes.reports import router as reports_router
from app.api.routes.settings import router as settings_router
from app.api.routes.scan import router as scan_router
from app.api.routes.service import router as service_router
from app.core.config import config
from app.database.session import init_db
from app.detectors.service import RDRSService
from app.web.dashboard import render_dashboard
from app.web.scanner_page import router as scanner_page_router


init_db()

monitoring_config = config.get("monitoring", {})
monitoring_paths = monitoring_config.get(
    "paths",
    ["./data/sandbox"],
)

service = RDRSService(
    paths=monitoring_paths,
)


@asynccontextmanager
async def lifespan(app: FastAPI):
    if not os.getenv("VERCEL"):
        service.start()

    yield

    if not os.getenv("VERCEL"):
        service.stop()


app = FastAPI(
    title="RDRS",
    description="Ransomware Detection & Response System",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(events_router)
app.include_router(incidents_router)
app.include_router(response_router)
app.include_router(reports_router)
app.include_router(settings_router)
app.include_router(service_router)
app.include_router(scan_router)
app.include_router(scanner_page_router)


@app.get("/")
def dashboard():
    return render_dashboard()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rdrs",
    }
