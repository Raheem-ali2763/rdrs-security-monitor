from datetime import datetime

from sqlalchemy import create_engine, inspect
from sqlalchemy.orm import Session

from app.database.incident_models import Evidence, Incident
from app.database.models import Base


def create_test_session():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)
    return Session(engine)


def test_incident_model_contains_expected_columns():
    columns = Incident.__table__.columns

    assert "id" in columns
    assert "incident_id" in columns
    assert "severity" in columns
    assert "threat_score" in columns
    assert "status" in columns
    assert "summary" in columns
    assert "started_at" in columns
    assert "ended_at" in columns


def test_evidence_model_contains_expected_columns():
    columns = Evidence.__table__.columns

    assert "id" in columns
    assert "incident_id" in columns
    assert "path" in columns
    assert "evidence_type" in columns
    assert "sha256" in columns
    assert "collected_at" in columns


def test_incident_and_evidence_can_be_stored_together():
    session = create_test_session()

    try:
        incident = Incident(
            incident_id="INC-2026-0001",
            severity="critical",
            threat_score=87.0,
            status="open",
            summary="Mass file modification detected.",
            started_at=datetime(2026, 8, 27, 15, 30, 0),
        )

        evidence = Evidence(
            path="data/sandbox/suspicious.bin",
            evidence_type="file",
            sha256="a" * 64,
        )

        incident.evidence.append(evidence)

        session.add(incident)
        session.commit()
        session.refresh(incident)

        assert incident.id is not None
        assert incident.incident_id == "INC-2026-0001"
        assert incident.severity == "critical"
        assert incident.threat_score == 87.0
        assert len(incident.evidence) == 1
        assert incident.evidence[0].path == "data/sandbox/suspicious.bin"
        assert incident.evidence[0].incident_id == incident.id
    finally:
        session.close()


def test_incident_and_evidence_tables_exist():
    engine = create_engine("sqlite:///:memory:")
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "incidents" in tables
    assert "evidence" in tables
