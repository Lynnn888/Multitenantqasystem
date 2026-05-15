# =========================
# FILE: app/routers/upload.py
# =========================

import os

from fastapi import APIRouter
from fastapi import UploadFile
from fastapi import File
from fastapi import Depends

from app.deps import get_db

from app.services.ingest_service import ingest_file

router = APIRouter()


@router.post("/upload/{tenant_id}")
async def upload_file(
    tenant_id: str,
    file: UploadFile = File(...),
    db=Depends(get_db)
):

    allowed = ["pdf", "md", "txt"]

    ext = file.filename.split(".")[-1].lower()

    if ext not in allowed:

        return {
            "error": "unsupported file type"
        }

    os.makedirs(
        f"tenant_data/{tenant_id}",
        exist_ok=True
    )

    filepath = (
        f"tenant_data/{tenant_id}/{file.filename}"
    )

    with open(filepath, "wb") as f:

        f.write(await file.read())

    ingest_file(
        db,
        tenant_id,
        filepath,
        file.filename
    )

    return {
        "message": "upload success"
    }