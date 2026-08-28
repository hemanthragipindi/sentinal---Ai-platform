from sqlalchemy import String, ForeignKey, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base

class AuditLog(Base):
    __tablename__ = "audit_logs"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    action: Mapped[str] = mapped_column(String, index=True, nullable=False)
    entity: Mapped[str] = mapped_column(String, index=True, nullable=False)
    entity_id: Mapped[str] = mapped_column(UUID(as_uuid=False), nullable=True)
    metadata_data: Mapped[dict] = mapped_column(JSONB, nullable=True)

    __table_args__ = (
        Index('ix_audit_logs_created_at', 'created_at'),
    )

class SystemLog(Base):
    __tablename__ = "system_logs"

    level: Mapped[str] = mapped_column(String, index=True, nullable=False)
    source: Mapped[str] = mapped_column(String, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    trace_id: Mapped[str] = mapped_column(String, nullable=True)
