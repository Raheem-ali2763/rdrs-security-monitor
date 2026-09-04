from pathlib import Path

import yaml
from fastapi import APIRouter, File, HTTPException, UploadFile

from app.detectors.incident_callback import persist_scan_incident
from app.scanner.scanner import FileScanner


router = APIRouter(prefix="/api/scan", tags=["scanner"])

scanner = FileScanner()


@router.post("")
async def scan_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    try:
        content = await file.read()

        destination = scanner.save_uploaded_file(
            file.filename,
            content,
        )

        result = scanner.scan(destination)

        persist_scan_incident(result)

        return {
            "status": "completed",
            "scan": result,
        }

    except FileNotFoundError as exc:
        raise HTTPException(
            status_code=404,
            detail=str(exc),
        ) from exc

    except ValueError as exc:
        raise HTTPException(
            status_code=413,
            detail=str(exc),
        ) from exc

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"File scan failed: {exc}",
        ) from exc


@router.get("/folders")
def scanner_folders():
    config_path = Path("config.yaml")

    config = {}
    if config_path.is_file():
        with config_path.open("r", encoding="utf-8") as file:
            config = yaml.safe_load(file) or {}

    scanner_config = config.get("scanner", {})

    incoming = Path(
        scanner_config.get(
            "incoming_directory",
            "./data/scanner/incoming",
        )
    )

    quarantine = Path(
        scanner_config.get(
            "quarantine_directory",
            "./data/quarantine/incidents",
        )
    )

    incoming.mkdir(parents=True, exist_ok=True)
    quarantine.mkdir(parents=True, exist_ok=True)

    def folder_info(path: Path) -> dict:
        files = [
            item
            for item in path.rglob("*")
            if item.is_file()
        ]

        return {
            "path": str(path.resolve()),
            "exists": path.is_dir(),
            "file_count": len(files),
            "files": [
                {
                    "name": item.name,
                    "path": str(item.relative_to(path)),
                    "size": item.stat().st_size,
                }
                for item in files[-50:]
            ],
        }

    return {
        "incoming": folder_info(incoming),
        "quarantine": folder_info(quarantine),
    }
