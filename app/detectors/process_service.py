from __future__ import annotations

from app.database.repository import ProcessRepository
from app.database.session import get_session
from app.detectors.process_telemetry import ProcessTelemetry


class ProcessTelemetryService:
    """Collect and persist defensive process telemetry."""

    def __init__(
        self,
        telemetry: ProcessTelemetry | None = None,
    ) -> None:
        self.telemetry = telemetry or ProcessTelemetry()

    def collect_and_persist(self) -> int:
        """Collect current process snapshots and persist them."""
        snapshots = self.telemetry.collect()

        session = get_session()

        try:
            repository = ProcessRepository(session)

            for snapshot in snapshots:
                repository.add(
                    pid=snapshot.pid,
                    name=snapshot.name,
                    cpu_percent=snapshot.cpu_percent,
                    memory_percent=snapshot.memory_percent,
                    disk_write_bytes=snapshot.disk_write_bytes,
                    executable=snapshot.executable,
                    parent_pid=snapshot.parent_pid,
                    parent_name=snapshot.parent_name,
                    unknown_process=snapshot.unknown_process,
                )

            return len(snapshots)

        finally:
            session.close()
