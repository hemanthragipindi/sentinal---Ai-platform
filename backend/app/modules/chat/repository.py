from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.chat.models import Conversation, Message

class ConversationRepository(BaseRepository[Conversation, dict, Any]):
    def __init__(self):
        super().__init__(Conversation)

    async def list_by_user(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
        stmt = select(Conversation).where(
            Conversation.user_id == user_id, 
            Conversation.deleted_at.is_(None)
        ).order_by(Conversation.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

class MessageRepository(BaseRepository[Message, dict, Any]):
    def __init__(self):
        super().__init__(Message)

    async def list_by_conversation(self, db: AsyncSession, conversation_id: str, skip: int = 0, limit: int = 100):
        stmt = select(Message).where(
            Message.conversation_id == conversation_id,
            Message.deleted_at.is_(None)
        ).order_by(Message.created_at.asc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

conversation_repo = ConversationRepository()
message_repo = MessageRepository()
