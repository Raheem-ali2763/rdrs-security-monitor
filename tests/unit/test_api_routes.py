from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_stats():
    r = client.get("/api/stats")
    assert r.status_code == 200


def test_events():
    r = client.get("/api/events?limit=6")
    assert r.status_code == 200


def test_incidents():
    r = client.get("/api/incidents")
    assert r.status_code == 200


def test_report_summary():
    r = client.get("/api/reports/summary")
    assert r.status_code == 200


def test_service_status():
    r = client.get("/api/service/status")
    assert r.status_code == 200


def test_settings():
    r = client.get("/api/settings")
    assert r.status_code == 200
