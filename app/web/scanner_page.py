from pathlib import Path

from fastapi import APIRouter
from fastapi.responses import FileResponse


router = APIRouter(tags=["scanner-ui"])

TEMPLATE_PATH = (
    Path(__file__).resolve().parent
    / "templates"
    / "scanner.html"
)


@router.get("/scanner", include_in_schema=False)
def scanner_page():
    return FileResponse(TEMPLATE_PATH)
