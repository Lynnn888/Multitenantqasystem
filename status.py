# =========================
# FILE: app/routers/status.py
# =========================

from fastapi import APIRouter
from fastapi import Depends

from app.deps import get_db

from app.models import Document

router = APIRouter()


@router.get("/status/{tenant_id}")
def get_status(
    tenant_id: str,
    db=Depends(get_db)
):

    docs = (
        db.query(Document)
        .filter(Document.tenant_id == tenant_id)
        .all()
    )

    return [
        {
            "filename": d.filename,
            "status": d.status
        }
        for d in docs
    ]