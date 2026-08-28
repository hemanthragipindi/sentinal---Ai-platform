from sqlalchemy import String, Integer, Float, ForeignKey, CheckConstraint
from sqlalchemy.dialects.postgresql import UUID, JSONB
from sqlalchemy.orm import Mapped, mapped_column

from app.database.models.base import Base

class UserSettings(Base):
    __tablename__ = "user_settings"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), unique=True, nullable=False)
    theme: Mapped[str] = mapped_column(String, nullable=True)
    default_model: Mapped[str] = mapped_column(String, nullable=True)
    temperature: Mapped[float] = mapped_column(Float, nullable=True)
    top_p: Mapped[float] = mapped_column(Float, nullable=True)
    max_tokens: Mapped[int] = mapped_column(Integer, nullable=True)

    __table_args__ = (
        CheckConstraint("temperature BETWEEN 0 AND 2", name="ck_settings_temperature"),
        CheckConstraint("top_p BETWEEN 0 AND 1", name="ck_settings_topp"),
    )

class SystemSetting(Base):
    __tablename__ = "system_settings"

    key: Mapped[str] = mapped_column(String, unique=True, index=True, nullable=False)
    value: Mapped[dict] = mapped_column(JSONB, nullable=False)
    description: Mapped[str] = mapped_column(String, nullable=True)
