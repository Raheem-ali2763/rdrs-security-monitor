from fastapi import APIRouter, HTTPException, UploadFile, File

from app.detectors.incident_callback import persist_scan_incident
from app.scanner.scanner import FileScanner


router = APIRouter(prefix="/scan", tags=["scanner"])

scanner = FileScanner()

MAX_SCAN_SIZE = 50 * 1024 * 1024  # 50 MB


@router.post("")
async def scan_file(file: UploadFile = File(...)):
    if not file.filename:
        raise HTTPException(
            status_code=400,
            detail="Filename is required",
        )

    try:
        content = await file.read()

        if len(content) > MAX_SCAN_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File is too large. Maximum scan size is 50 MB.",
            )

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

    except HTTPException:
        raise

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
