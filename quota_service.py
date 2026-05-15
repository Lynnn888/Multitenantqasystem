# =========================
# FILE: app/services/quota_service.py
# =========================

from fastapi import HTTPException

from app.models import Usage

from app.config import settings


def check_quota(
    db,
    tenant_id: str,
    tokens_needed: int
):

    usage = (
        db.query(Usage)
        .filter(Usage.tenant_id == tenant_id)
        .first()
    )

    if not usage:

        usage = Usage(
            tenant_id=tenant_id,
            tokens_used=0
        )

        db.add(usage)

        db.commit()

    if (
        usage.tokens_used + tokens_needed
        > settings.MAX_TOKENS_PER_TENANT
    ):

        raise HTTPException(
            status_code=429,
            detail=f"Tenant {tenant_id} exceeded token quota"
        )

    usage.tokens_used += tokens_needed

    db.commit()