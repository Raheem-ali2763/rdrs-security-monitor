from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.api.routes.events import router as events_router
from app.api.routes.incidents import router as incidents_router
from app.api.routes.reports import router as reports_router
from app.api.routes.settings import router as settings_router
from app.api.routes.service import router as service_router
from app.detectors.service import RDRSService
from app.web.dashboard import render_dashboard


service = RDRSService(paths=["data/sandbox"])


@asynccontextmanager
async def lifespan(app: FastAPI):
    service.start()
    yield
    service.stop()


app = FastAPI(
    title="RDRS",
    description="Ransomware Detection & Response System",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(events_router)
app.include_router(incidents_router)
app.include_router(reports_router)
app.include_router(settings_router)
app.include_router(service_router)


@app.get("/")
def dashboard():
    return render_dashboard()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rdrs",
    }
