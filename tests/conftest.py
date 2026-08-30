import pytest

from app.database.models import Base
from app.database.incident_models import Incident, Evidence
from app.database.session import engine


@pytest.fixture(scope="session", autouse=True)
def create_database_tables():
    Base.metadata.create_all(bind=engine)
    yield
