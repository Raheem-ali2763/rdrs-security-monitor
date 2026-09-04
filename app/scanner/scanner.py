from __future__ import annotations

import re
import shutil
from pathlib import Path
from uuid import uuid4

import yaml

from .analyzer import analyze_file


class FileScanner:
    """Safe on-demand file scanner with quarantine support."""

    def __init__(
        self,
        incoming_dir: str | None = None,
        quarantine_dir: str | None = None,
        max_file_size_mb: int | None = None,
    ):
        config_path = Path("config.yaml")
        config = {}

        if config_path.is_file():
            with config_path.open("r", encoding="utf-8") as file:
                config = yaml.safe_load(file) or {}

        scanner_config = config.get("scanner", {})

        self.incoming_dir = Path(
            incoming_dir
            or scanner_config.get(
                "incoming_directory",
                "./data/scanner/incoming",
            )
        )

        self.quarantine_dir = Path(
            quarantine_dir
            or scanner_config.get(
                "quarantine_directory",
                "./data/quarantine/incidents",
            )
        )

        self.max_file_size_mb = int(
            max_file_size_mb
            or scanner_config.get("max_file_size_mb", 50)
        )

        self.max_file_size_bytes = self.max_file_size_mb * 1024 * 1024

        self.incoming_dir.mkdir(parents=True, exist_ok=True)
        self.quarantine_dir.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def safe_filename(filename: str) -> str:
        """Return a safe filename without directory traversal."""
        name = Path(filename).name
        name = re.sub(r"[^A-Za-z0-9._-]", "_", name)

        if not name or name in {".", ".."}:
            name = "uploaded_file"

        return name

    def save_uploaded_file(self, filename: str, content: bytes) -> Path:
        """Save an uploaded file inside the scanner incoming directory."""
        if len(content) > self.max_file_size_bytes:
            raise ValueError(
                f"File is too large. Maximum scan size is "
                f"{self.max_file_size_mb} MB."
            )

        safe_name = self.safe_filename(filename)
        destination = self.incoming_dir / safe_name

        destination.write_bytes(content)

        return destination

    def scan(self, file_path: str | Path) -> dict:
        """Analyze a file and return its security assessment."""
        path = Path(file_path)

        if not path.is_file():
            raise FileNotFoundError(f"File not found: {path}")

        if path.stat().st_size > self.max_file_size_bytes:
            raise ValueError(
                f"File is too large. Maximum scan size is "
                f"{self.max_file_size_mb} MB."
            )

        result = analyze_file(path)

        result["scan_id"] = str(uuid4())
        result["quarantined"] = False
        result["quarantine_path"] = None

        if result["severity"] == "Critical":
            result["quarantine_path"] = self._quarantine(
                path,
                result["scan_id"],
            )
            result["quarantined"] = True

        return result

    def _quarantine(self, source: Path, scan_id: str) -> str:
        """Copy suspicious evidence without modifying the original."""
        incident_dir = self.quarantine_dir / scan_id
        incident_dir.mkdir(parents=True, exist_ok=True)

        safe_name = self.safe_filename(source.name)
        destination = incident_dir / safe_name

        shutil.copy2(source, destination)

        return str(destination.resolve())

    def quarantine_file(
        self,
        file_path: str | Path,
        incident_id: str | None = None,
    ) -> str:
        """Manually copy a file into an incident quarantine directory."""
        source = Path(file_path)

        if not source.is_file():
            raise FileNotFoundError(f"File not found: {source}")

        quarantine_id = incident_id or str(uuid4())

        return self._quarantine(source, quarantine_id)
