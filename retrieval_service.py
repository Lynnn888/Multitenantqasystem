# =========================
# FILE: app/services/retrieval_service.py
# =========================

import time
import numpy as np

from rank_bm25 import BM25Okapi

from sentence_transformers import SentenceTransformer

from app.config import settings

from app.services.ingest_service import tenant_indexes
from app.services.ingest_service import tenant_chunk_map

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)


def reciprocal_rank_fusion(
    vector_rank,
    keyword_rank,
    k=60
):

    scores = {}

    for rank, idx in enumerate(vector_rank):

        scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

    for rank, idx in enumerate(keyword_rank):

        scores[idx] = scores.get(idx, 0) + 1 / (k + rank)

    ranked = sorted(
        scores,
        key=scores.get,
        reverse=True
    )

    return ranked


def retrieve(
    tenant_id: str,
    query: str,
    top_k: int = settings.TOP_K
):

    start = time.time()

    if tenant_id not in tenant_indexes:

        return [], 0

    chunks = tenant_chunk_map[tenant_id]

    # BM25

    tokenized_docs = [
        c.split()
        for c in chunks
    ]

    bm25 = BM25Okapi(tokenized_docs)

    bm25_scores = bm25.get_scores(query.split())

    keyword_rank = np.argsort(bm25_scores)[::-1]

    # Vector Search

    query_embedding = embedding_model.encode(
        [query]
    ).astype("float32")

    index = tenant_indexes[tenant_id]

    _, vector_rank = index.search(
        query_embedding,
        top_k
    )

    vector_rank = vector_rank[0]

    # RRF

    fused_rank = reciprocal_rank_fusion(
        vector_rank,
        keyword_rank[:top_k]
    )

    results = []

    for idx in fused_rank[:top_k]:

        if idx < len(chunks):

            results.append(chunks[idx])

    retrieval_time = time.time() - start

    return results, retrieval_time