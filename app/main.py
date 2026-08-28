from fastapi import FastAPI
from app.web.dashboard import render_dashboard

app = FastAPI(
    title="RDRS",
    description="Ransomware Detection & Response System",
    version="0.1.0",
)

@app.get("/")
def dashboard():
    return render_dashboard()

@app.get("/health")
def health() -> dict[str, str]:
    return {
        "status": "ok",
        "service": "rdrs",
    }
