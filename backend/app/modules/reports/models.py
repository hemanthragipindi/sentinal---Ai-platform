from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base
from app.database.models.enums import ReportStatus

class Report(Base):
    __tablename__ = "reports"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), index=True, nullable=True)
    title: Mapped[str] = mapped_column(String, nullable=False)
    report_type: Mapped[str] = mapped_column(String, index=True, nullable=False)
    content: Mapped[dict] = mapped_column(JSONB, nullable=False)
    status: Mapped[ReportStatus] = mapped_column(Enum(ReportStatus, name="report_status", create_type=True, values_callable=lambda obj: [e.value for e in obj]), index=True, nullable=False)
    
    generated_by: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    generated_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    download_url: Mapped[str] = mapped_column(String, nullable=True)

    __table_args__ = (
        Index('ix_reports_created_at', 'created_at'),
    )

class UsageStatistic(Base):
    __tablename__ = "usage_statistics"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    metric_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    metric_value: Mapped[int] = mapped_column(Integer, nullable=False)
    period: Mapped[str] = mapped_column(String, nullable=False)
