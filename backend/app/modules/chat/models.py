from typing import List
from datetime import datetime
from sqlalchemy import String, Integer, ForeignKey, Enum, Index
from sqlalchemy.dialects.postgresql import UUID, JSONB, TIMESTAMP
from sqlalchemy.orm import Mapped, mapped_column, relationship

from app.database.models.base import Base
from app.database.models.enums import ConversationStatus, MessageRole

class Conversation(Base):
    __tablename__ = "conversations"

    user_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("users.id", ondelete="CASCADE"), index=True, nullable=False)
    title: Mapped[str] = mapped_column(String, nullable=False)
    model_name: Mapped[str] = mapped_column(String, nullable=False)
    status: Mapped[ConversationStatus] = mapped_column(Enum(ConversationStatus, name="conversation_status", create_type=True, values_callable=lambda obj: [e.value for e in obj]), server_default=ConversationStatus.ACTIVE.value, nullable=False)
    
    total_tokens: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    message_count: Mapped[int] = mapped_column(Integer, server_default="0", nullable=False)
    last_message_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), index=True, nullable=True)

    # Relationships
    messages: Mapped[List["Message"]] = relationship("Message", back_populates="conversation", cascade="all, delete-orphan")

class Message(Base):
    __tablename__ = "messages"

    conversation_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("conversations.id", ondelete="CASCADE"), index=True, nullable=False)
    role: Mapped[MessageRole] = mapped_column(Enum(MessageRole, name="message_role", create_type=True, values_callable=lambda obj: [e.value for e in obj]), nullable=False)
    content: Mapped[str] = mapped_column(String, nullable=False)
    
    metadata_data: Mapped[dict] = mapped_column(JSONB, nullable=True)
    finish_reason: Mapped[str] = mapped_column(String, nullable=True)
    response_time_ms: Mapped[int] = mapped_column(Integer, nullable=True)
    model_name: Mapped[str] = mapped_column(String, nullable=True)
    
    prompt_tokens: Mapped[int] = mapped_column(Integer, nullable=True)
    completion_tokens: Mapped[int] = mapped_column(Integer, nullable=True)
    total_tokens: Mapped[int] = mapped_column(Integer, nullable=True)

    # Relationships
    conversation: Mapped["Conversation"] = relationship("Conversation", back_populates="messages")
    attachments: Mapped[List["MessageAttachment"]] = relationship("MessageAttachment", back_populates="message", cascade="all, delete-orphan")

    __table_args__ = (
        Index('ix_messages_created_at', 'created_at'),
    )

class MessageAttachment(Base):
    __tablename__ = "message_attachments"

    message_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("messages.id", ondelete="CASCADE"), index=True, nullable=False)
    file_id: Mapped[str] = mapped_column(UUID(as_uuid=False), ForeignKey("files.id", ondelete="CASCADE"), nullable=False)

    message: Mapped["Message"] = relationship("Message", back_populates="attachments")
