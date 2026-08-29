from pathlib import Path

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from app.database.models import Base
from app.detectors.base import FileEvent
from app.detectors.service import RDRSService
import app.detectors.service as service_module


def test_service_processes_file_event(tmp_path, capsys, monkeypatch):
    db_path = tmp_path / "test.db"
    engine = create_engine(
        f"sqlite:///{db_path}",
        connect_args={"check_same_thread": False},
    )

    Base.metadata.create_all(engine)

    TestSession = sessionmaker(
        bind=engine,
        autoflush=False,
        autocommit=False,
    )

    monkeypatch.setattr(
        service_module,
        "get_session",
        lambda: TestSession(),
    )

    path = tmp_path / "suspicious.bin"
    path.write_bytes(bytes(range(256)) * 10)

    service = RDRSService([str(tmp_path)])

    event = FileEvent.create(
        event_type="create",
        path=path,
    )

    service._handle_event(event)

    output = capsys.readouterr().out

    assert "[RDRS] CREATE" in output
    assert str(path) in output
    assert "entropy=8.00" in output
    assert "suspicious=True" in output
    assert "high_entropy" in output


def test_service_creates_monitor_with_configured_path(tmp_path):
    service = RDRSService([str(tmp_path)])

    assert len(service.monitor.paths) == 1
    assert service.monitor.paths[0] == Path(tmp_path)

