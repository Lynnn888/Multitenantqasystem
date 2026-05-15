# =========================
# FILE: app/models.py
# =========================

from sqlalchemy import Column
from sqlalchemy import Integer
from sqlalchemy import String
from sqlalchemy import Text
from sqlalchemy import Float

from app.database import Base


class Document(Base):

    __tablename__ = "documents"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(String, index=True)

    filename = Column(String)

    status = Column(String, default="pending")


class Chunk(Base):

    __tablename__ = "chunks"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(String, index=True)

    document_id = Column(Integer)

    content = Column(Text)


class Usage(Base):

    __tablename__ = "usage"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(String, unique=True)

    tokens_used = Column(Integer, default=0)


class Metrics(Base):

    __tablename__ = "metrics"

    id = Column(Integer, primary_key=True)

    tenant_id = Column(String)

    question = Column(Text)

    retrieval_time = Column(Float)

    generation_time = Column(Float)

    chunk_count = Column(Integer)

    token_usage = Column(Integer)