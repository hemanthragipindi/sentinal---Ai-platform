from sqlalchemy import String, Integer, text, Float, Boolean, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base

class PromptTemplate(Base):
    __tablename__ = "prompt_templates"

    name: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
    template: Mapped[str] = mapped_column(String, nullable=False)
    version: Mapped[int] = mapped_column(Integer, server_default=text("1"), nullable=False)
    status: Mapped[str] = mapped_column(String, server_default=text("'active'"), nullable=False)

class ModelUsageLog(Base):
    __tablename__ = "model_usage_logs"

    model_name: Mapped[str] = mapped_column(String, index=True, nullable=False)
    request_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    response_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=False)
    latency_ms: Mapped[int] = mapped_column(Integer, nullable=False)
    
    provider: Mapped[str] = mapped_column(String, nullable=True)
    model_version: Mapped[str] = mapped_column(String, nullable=True)
    estimated_cost: Mapped[float] = mapped_column(Float, nullable=True)
    cache_hit: Mapped[bool] = mapped_column(Boolean, server_default=text("false"), nullable=False)
