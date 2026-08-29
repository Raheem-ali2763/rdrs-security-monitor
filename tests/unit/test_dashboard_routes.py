from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_dashboard():
    r = client.get("/")
    assert r.status_code == 200
    assert "RDRS" in r.text


def test_health():
    r = client.get("/health")
    assert r.status_code == 200
    assert r.json()["status"] == "ok"
