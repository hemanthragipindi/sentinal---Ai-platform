from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum, Index, CheckConstraint, text
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.enums import JobStatus

class Job(Base):
    __tablename__ = "jobs"

    name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[JobStatus] = mapped_column(Enum(JobStatus, name="job_status", create_type=True, values_callable=lambda obj: [e.value for e in obj]), index=True, nullable=False)
    payload: Mapped[dict] = mapped_column(JSONB, nullable=True)
    
    started_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    completed_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), nullable=True)
    retry_count: Mapped[int] = mapped_column(Integer, server_default=text("0"), nullable=False)
    error_message: Mapped[str] = mapped_column(String, nullable=True)

    # Relationships
    logs: Mapped[List["JobLog"]] = relationship("JobLog", back_populates="job", cascade="all, delete-orphan")

    __table_args__ = (
        CheckConstraint("retry_count >= 0", name="ck_jobs_retry_count"),
        Index('ix_jobs_created_at', 'created_at'),
    )

class JobLog(Base):
    __tablename__ = "job_logs"

    job_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("jobs.id", ondelete="CASCADE"), index=True, nullable=False)
    message: Mapped[str] = mapped_column(String, nullable=False)
    level: Mapped[str] = mapped_column(String, nullable=False)

    job: Mapped["Job"] = relationship("Job", back_populates="logs")
