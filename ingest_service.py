# =========================
# FILE: app/services/ingest_service.py
# =========================

import numpy as np
import faiss

from sentence_transformers import SentenceTransformer

from app.models import Document
from app.models import Chunk

from app.utils.chunker import chunk_text
from app.utils.pdf_loader import load_pdf

embedding_model = SentenceTransformer(
    "sentence-transformers/all-MiniLM-L6-v2"
)

tenant_indexes = {}

tenant_chunk_map = {}


def get_or_create_index(tenant_id: str):

    if tenant_id not in tenant_indexes:

        tenant_indexes[tenant_id] = faiss.IndexFlatL2(384)

        tenant_chunk_map[tenant_id] = []

    return tenant_indexes[tenant_id]


def ingest_file(
    db,
    tenant_id: str,
    filepath: str,
    filename: str
):

    doc = Document(
        tenant_id=tenant_id,
        filename=filename,
        status="processing"
    )

    db.add(doc)

    db.commit()

    db.refresh(doc)

    try:

        ext = filename.split(".")[-1].lower()

        if ext == "pdf":

            text = load_pdf(filepath)

        else:

            with open(filepath, "r", encoding="utf-8") as f:

                text = f.read()

        chunks = chunk_text(text)

        embeddings = embedding_model.encode(chunks)

        index = get_or_create_index(tenant_id)

        index.add(
            np.array(embeddings).astype("float32")
        )

        for chunk in chunks:

            db_chunk = Chunk(
                tenant_id=tenant_id,
                document_id=doc.id,
                content=chunk
            )

            db.add(db_chunk)

            tenant_chunk_map[tenant_id].append(chunk)

        doc.status = "done"

        db.commit()

    except Exception as e:

        doc.status = "failed"

        db.commit()

        raise e