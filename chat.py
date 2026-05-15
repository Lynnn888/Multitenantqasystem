# =========================
# FILE: app/routers/chat.py
# =========================

import time

from fastapi import APIRouter
from fastapi import Depends

from fastapi.responses import StreamingResponse

from app.schemas import ChatRequest

from app.deps import get_db

from app.utils.sse import format_sse

from app.services.retrieval_service import retrieve

from app.services.llm_service import stream_llm_response

from app.services.quota_service import check_quota

from app.services.metrics_service import save_metrics

router = APIRouter()


@router.post("/chat/{tenant_id}")
async def chat(
    tenant_id: str,
    body: ChatRequest,
    db=Depends(get_db)
):

    question = body.question

    estimated_tokens = len(question.split()) * 2

    check_quota(
        db,
        tenant_id,
        estimated_tokens
    )

    retrieved_chunks, retrieval_time = retrieve(
        tenant_id,
        question
    )

    context = "\n".join(retrieved_chunks)

    async def event_generator():

        generation_start = time.time()

        yield format_sse(
            f"retrieval_time={retrieval_time}"
        )

        yield format_sse(
            f"chunks_used={len(retrieved_chunks)}"
        )

        async for token in stream_llm_response(
            question,
            context
        ):

            yield format_sse(token)

        generation_time = (
            time.time() - generation_start
        )

        save_metrics(
            db=db,
            tenant_id=tenant_id,
            question=question,
            retrieval_time=retrieval_time,
            generation_time=generation_time,
            chunk_count=len(retrieved_chunks),
            token_usage=estimated_tokens
        )

        yield format_sse(
            f"generation_time={generation_time}"
        )

    return StreamingResponse(
        event_generator(),
        media_type="text/event-stream"
    )