from sqlalchemy import String, Integer, BigInteger, text, ForeignKey, CheckConstraint, Enum, Index
from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy.dialects.postgresql import UUID

from app.database.models.base import Base
from app.database.models.enums import FileAccessAction

class File(Base):
    __tablename__ = "files"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    bucket: Mapped[str] = mapped_column(String, nullable=False)
    file_name: Mapped[str] = mapped_column(String, nullable=False)
    storage_path: Mapped[str] = mapped_column(String, unique=True, nullable=False)
    mime_type: Mapped[str] = mapped_column(String, nullable=False)
    file_size: Mapped[int] = mapped_column(BigInteger, nullable=False)
    public_url: Mapped[str] = mapped_column(String, nullable=True)

    __table_args__ = (
        CheckConstraint("file_size >= 0", name="ck_files_file_size_positive"),
        Index('ix_files_user_id', 'user_id'),
    )

class FileAccessLog(Base):
    __tablename__ = "file_access_logs"

    file_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("files.id", ondelete="CASCADE"), index=True, nullable=False)
    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="SET NULL"), nullable=True)
    action: Mapped[FileAccessAction] = mapped_column(Enum(FileAccessAction, name="file_access_action", create_type=True, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    ip_address: Mapped[str] = mapped_column(String, nullable=True)
