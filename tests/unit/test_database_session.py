from pathlib import Path

from sqlalchemy import inspect, text

from app.database.models import Base, Event
from app.database.session import DATABASE_PATH, engine, get_session


def test_database_path_is_inside_data_directory():
    assert DATABASE_PATH.parent.name == "data"
    assert DATABASE_PATH.name == "rdrs.db"


def test_database_connection_works():
    with engine.connect() as connection:
        result = connection.execute(text("SELECT 1")).scalar_one()

    assert result == 1


def test_database_creates_events_table():
    Base.metadata.create_all(bind=engine)

    inspector = inspect(engine)
    tables = inspector.get_table_names()

    assert "events" in tables


def test_get_session_returns_sqlalchemy_session():
    session = get_session()

    try:
        assert session.bind is engine
    finally:
        session.close()
