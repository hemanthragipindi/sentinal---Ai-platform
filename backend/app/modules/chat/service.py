from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone
import logging

from app.modules.chat.repository import conversation_repo, message_repo
from app.modules.chat.schemas import ConversationCreate, MessageCreate
from app.modules.chat.models import Conversation, Message
from app.core.exceptions import SentinelException
from app.database.models.enums import ConversationStatus
from app.ai.llm.factory import LLMFactory

logger = logging.getLogger(__name__)

class ChatService:
    async def create_conversation(self, db: AsyncSession, user_id: str, obj_in: ConversationCreate) -> Conversation:
        data = obj_in.model_dump()
        data["user_id"] = user_id
        data["status"] = ConversationStatus.ACTIVE
        
        conv = await conversation_repo.create(db, data)
        await db.commit()
        return conv

    async def get_conversation(self, db: AsyncSession, user_id: str, conv_id: str) -> Conversation:
        conv = await conversation_repo.get_by_id(db, conv_id)
        if not conv or str(conv.user_id) != str(user_id):
            raise SentinelException("Conversation not found", status_code=404)
        return conv

    async def update_conversation(self, db: AsyncSession, user_id: str, conv_id: str, update_in) -> Conversation:
        conv = await self.get_conversation(db, user_id, conv_id)
        update_data = update_in.model_dump(exclude_unset=True)
        updated_conv = await conversation_repo.update(db, conv, update_data)
        await db.commit()
        return updated_conv

    async def delete_conversation(self, db: AsyncSession, user_id: str, conv_id: str) -> None:
        conv = await self.get_conversation(db, user_id, conv_id)
        await conversation_repo.soft_delete(db, conv.id)
        await db.commit()

    async def send_message(self, db: AsyncSession, user_id: str, conv_id: str, obj_in: MessageCreate) -> Message:
        # Verify ownership
        conv = await self.get_conversation(db, user_id, conv_id)
        
        # 1. Save User Message
        msg_data = obj_in.model_dump()
        msg_data["conversation_id"] = conv.id
        await message_repo.create(db, msg_data)
        
        # 2. Get past messages to send to LLM
        past_msgs = await message_repo.list_by_conversation(db, conv_id, skip=0, limit=20)
        messages_for_llm = []
        for m in reversed(past_msgs):
            messages_for_llm.append({"role": m.role, "content": m.content})
            
        # 3. Generate AI Response
        ai_response_text = "I'm sorry, I couldn't process your request at this time."
        try:
            llm_client = LLMFactory.get_llm()
            ai_response_text = await llm_client.chat(messages_for_llm)
        except Exception as e:
            logger.error(f"LLM Generation Error: {e}")
            # We will still save the fallback error message so the user sees it
        
        # 4. Save AI Message
        ai_msg_data = {
            "conversation_id": conv.id,
            "role": "assistant",
            "content": ai_response_text
        }
        ai_msg = await message_repo.create(db, ai_msg_data)
        
        # Update conversation stats
        conv.message_count += 2
        conv.last_message_at = datetime.now(timezone.utc)
        await db.commit()
        
        return ai_msg

chat_service = ChatService()
