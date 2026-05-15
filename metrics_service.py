# =========================
# FILE: app/services/metrics_service.py
# =========================

from app.models import Metrics


def save_metrics(
    db,
    tenant_id,
    question,
    retrieval_time,
    generation_time,
    chunk_count,
    token_usage
):

    metric = Metrics(
        tenant_id=tenant_id,
        question=question,
        retrieval_time=retrieval_time,
        generation_time=generation_time,
        chunk_count=chunk_count,
        token_usage=token_usage
    )

    db.add(metric)

    db.commit()