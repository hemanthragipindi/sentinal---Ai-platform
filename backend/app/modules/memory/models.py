from typing import List
from datetime import datetime
from sqlalchemy import String, Float, Integer, ForeignKey, Enum, CheckConstraint, Index
from sqlalchemy.orm import Mapped, mapped_column, relationship
from sqlalchemy.dialects.postgresql import UUID, TIMESTAMP
from pgvector.sqlalchemy import Vector

from app.database.models.base import Base
from app.database.models.enums import MemoryType, MemoryStatus

class Memory(Base):
    __tablename__ = "memories"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("conversations.id", ondelete="SET NULL"), index=True, nullable=True)
    
    title: Mapped[str] = mapped_column(String, nullable=True)
    content: Mapped[str] = mapped_column(String, nullable=False)
    summary: Mapped[str] = mapped_column(String, nullable=True)
    
    memory_type: Mapped[MemoryType] = mapped_column(Enum(MemoryType, name="memory_type", create_type=True, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    importance_score: Mapped[float] = mapped_column(Float, nullable=True)
    confidence_score: Mapped[float] = mapped_column(Float, nullable=True)
    trust_score: Mapped[float] = mapped_column(Float, nullable=True)
    
    status: Mapped[MemoryStatus] = mapped_column(Enum(MemoryStatus, name="memory_status", create_type=True, values_callable=lambda obj: [e.value for e in obj]), server_default=MemoryStatus.ACTIVE.value, nullable=False)
    embedding_status: Mapped[str] = mapped_column(String, nullable=True)
    source: Mapped[str] = mapped_column(String, nullable=True)
    visibility: Mapped[str] = mapped_column(String, nullable=True)
    expires_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    version: Mapped[int] = mapped_column(Integer, nullable=False, server_default="1", default=1)

    # Relationships
    embeddings: Mapped[List["MemoryEmbedding"]] = relationship("MemoryEmbedding", back_populates="memory", cascade="all, delete-orphan")
    versions: Mapped[List["MemoryVersion"]] = relationship("MemoryVersion", back_populates="memory", cascade="all, delete-orphan")
    provenance: Mapped["MemoryProvenance"] = relationship("MemoryProvenance", back_populates="memory", uselist=False, cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("importance_score BETWEEN 0 AND 1", name="ck_memories_importance"),
        CheckConstraint("confidence_score BETWEEN 0 AND 1", name="ck_memories_confidence"),
        CheckConstraint("trust_score BETWEEN 0 AND 1", name="ck_memories_trust"),
        Index('ix_memories_created_at', 'created_at'),
    )

class MemoryProvenance(Base):
    __tablename__ = "memory_provenances"

    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False, unique=True)
    source_type: Mapped[str] = mapped_column(String, nullable=False)
    original_content_hash: Mapped[str] = mapped_column(String, nullable=False)
    
    memory: Mapped["Memory"] = relationship("Memory", back_populates="provenance")

class MemoryEmbedding(Base):
    __tablename__ = "memory_embeddings"

    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False)
    embedding: Mapped[str] = mapped_column(Vector(768), nullable=False)
    embedding_model: Mapped[str] = mapped_column(String, nullable=False)

    memory: Mapped["Memory"] = relationship("Memory", back_populates="embeddings")

    __table_args__ = (
        Index('ix_memory_embeddings_hnsw', 'embedding', postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'}),
    )

class MemoryVersion(Base):
    __tablename__ = "memory_versions"

    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False)
    version: Mapped[int] = mapped_column(Integer, nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    content_hash: Mapped[str] = mapped_column(String, nullable=False)
    change_reason: Mapped[str] = mapped_column(String, nullable=True)

    memory: Mapped["Memory"] = relationship("Memory", back_populates="versions")

class RetrievalLog(Base):
    __tablename__ = "retrieval_logs"

    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("conversations.id", ondelete="SET NULL"), index=True, nullable=True)
    query: Mapped[str] = mapped_column(String, nullable=False)
    top_k: Mapped[int] = mapped_column(Integer, nullable=False)
    response_time: Mapped[float] = mapped_column(Float, nullable=True)

    retrieved_memories: Mapped[List["RetrievedMemory"]] = relationship("RetrievedMemory", back_populates="retrieval_log", cascade="all, delete-orphan")
    
    __table_args__ = (
        Index('ix_retrieval_logs_created_at', 'created_at'),
    )

class RetrievedMemory(Base):
    __tablename__ = "retrieved_memories"

    retrieval_log_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("retrieval_logs.id", ondelete="CASCADE"), index=True, nullable=False)
    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), nullable=False)
    similarity_score: Mapped[float] = mapped_column(Float, nullable=False)
    rank: Mapped[int] = mapped_column(Integer, nullable=False)

    retrieval_log: Mapped["RetrievalLog"] = relationship("RetrievalLog", back_populates="retrieved_memories")
