from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

import psutil


@dataclass(frozen=True, slots=True)
class ProcessSnapshot:
    pid: int
    name: str
    cpu_percent: float
    memory_percent: float
    disk_write_bytes: int
    executable: str | None
    parent_pid: int | None
    parent_name: str | None
    unknown_process: bool = False


class ProcessTelemetry:
    """Collect defensive process telemetry using psutil."""

    def __init__(
        self,
        cpu_threshold_percent: float = 80.0,
        known_processes: set[str] | None = None,
    ) -> None:
        self.cpu_threshold_percent = cpu_threshold_percent
        self.known_processes = {
            name.lower()
            for name in (known_processes or set())
        }

    def snapshot(self, process: psutil.Process) -> ProcessSnapshot:
        try:
            name = process.name()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            name = "unknown"

        try:
            cpu_percent = process.cpu_percent(interval=0.0)
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            cpu_percent = 0.0

        try:
            memory_percent = process.memory_percent()
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            memory_percent = 0.0

        try:
            io = process.io_counters()
            disk_write_bytes = io.write_bytes
        except (
            psutil.NoSuchProcess,
            psutil.AccessDenied,
            AttributeError,
        ):
            disk_write_bytes = 0

        try:
            executable = process.exe()
        except (psutil.NoSuchProcess, psutil.AccessDenied, OSError):
            executable = None

        try:
            parent = process.parent()
            parent_pid = parent.pid if parent else None
            parent_name = parent.name() if parent else None
        except (psutil.NoSuchProcess, psutil.AccessDenied):
            parent_pid = None
            parent_name = None

        unknown_process = (
            bool(self.known_processes)
            and name.lower() not in self.known_processes
        )

        return ProcessSnapshot(
            pid=process.pid,
            name=name,
            cpu_percent=round(cpu_percent, 2),
            memory_percent=round(memory_percent, 2),
            disk_write_bytes=disk_write_bytes,
            executable=executable,
            parent_pid=parent_pid,
            parent_name=parent_name,
            unknown_process=unknown_process,
        )

    def collect(self) -> list[ProcessSnapshot]:
        """Collect snapshots for currently running processes."""
        snapshots: list[ProcessSnapshot] = []

        for process in psutil.process_iter(
            ["pid", "name"]
        ):
            try:
                snapshots.append(self.snapshot(process))
            except (
                psutil.NoSuchProcess,
                psutil.AccessDenied,
            ):
                continue

        return snapshots

    def is_cpu_spike(self, snapshot: ProcessSnapshot) -> bool:
        """Return whether a process exceeds the configured CPU threshold."""
        return snapshot.cpu_percent >= self.cpu_threshold_percent

    @staticmethod
    def executable_name(snapshot: ProcessSnapshot) -> str | None:
        """Return the executable filename when available."""
        if not snapshot.executable:
            return None

        return Path(snapshot.executable).name
