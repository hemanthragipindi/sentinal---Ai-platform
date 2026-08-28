from datetime import datetime
from sqlalchemy import String, Float, ForeignKey, Enum, CheckConstraint, Index, Boolean, text, Integer
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base
from app.database.models.enums import ThreatSeverity, ThreatStatus, SecurityEventSeverity

class Threat(Base):
    __tablename__ = "threats"

    title: Mapped[str] = mapped_column(String, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    severity: Mapped[ThreatSeverity] = mapped_column(Enum(ThreatSeverity, name="threat_severity", create_type=True, values_callable=lambda obj: [e.value for e in obj]), index=True, nullable=False)
    status: Mapped[ThreatStatus] = mapped_column(Enum(ThreatStatus, name="threat_status", create_type=True, values_callable=lambda obj: [e.value for e in obj]), index=True, nullable=False)

class AnomalyResult(Base):
    __tablename__ = "anomaly_results"

    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), index=True, nullable=False)
    memory_version: Mapped[int] = mapped_column(Integer, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    is_suspicious: Mapped[bool] = mapped_column(Boolean, default=False)
    signals: Mapped[dict] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 1", name="ck_anomaly_score_range"),
    )

class TrustScore(Base):
    __tablename__ = "trust_scores"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    score: Mapped[float] = mapped_column(Float, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=True)
    
    __table_args__ = (
        CheckConstraint("score BETWEEN 0 AND 1", name="ck_trust_score_range"),
    )

class QuarantinedMemory(Base):
    __tablename__ = "quarantined_memories"

    memory_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("memories.id", ondelete="CASCADE"), unique=True, nullable=False)
    reason: Mapped[str] = mapped_column(String, nullable=False)
    reviewed_by: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    status: Mapped[str] = mapped_column(String, index=True, nullable=False)

class SecurityEvent(Base):
    __tablename__ = "security_events"

    event_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    metadata_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    severity: Mapped[SecurityEventSeverity] = mapped_column(Enum(SecurityEventSeverity, name="security_event_severity", create_type=True, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=True)
    resolved: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), nullable=False)
    resolved_by: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    resolved_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)

    __table_args__ = (
        Index('ix_security_events_created_at', 'created_at'),
    )
