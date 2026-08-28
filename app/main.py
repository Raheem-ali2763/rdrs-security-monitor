from fastapi import FastAPI

from app.api.routes.events import router as events_router
from app.api.routes.incidents import router as incidents_router
from app.web.dashboard import render_dashboard


app = FastAPI(
    title="RDRS",
    description="Ransomware Detection & Response System",
    version="0.1.0",
)

app.include_router(events_router)
app.include_router(incidents_router)


@app.get("/")
def dashboard():
    return render_dashboard()


@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rdrs",
    }
