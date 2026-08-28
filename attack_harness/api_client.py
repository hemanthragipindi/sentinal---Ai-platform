import sys
import os
import asyncio

# Ensure backend can be imported
backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.core.database import AsyncSessionLocal
from app.modules.memory.service import memory_service
from app.modules.chat.service import chat_service
from app.modules.retrieval.service import retrieval_service

from app.modules.memory.schemas import MemoryCreate, MemoryUpdate
from app.modules.chat.schemas import ConversationCreate, MessageCreate
from app.modules.retrieval.schemas import RetrievalQuery
from app.database.models.enums import MessageRole, MemoryType

class SentinelAPIClient:
    """
    Directly interacts with Sentinel's backend service layer by managing
    its own DB sessions. This simulates an attacker with deep access
    or provides a clean testing interface without HTTP overhead.
    """
    
    def __init__(self, user_id: str):
        self.user_id = user_id

    async def _execute(self, func, *args, **kwargs):
        async with AsyncSessionLocal() as db:
            result = await func(db, *args, **kwargs)
            return result

    async def create_memory(self, title: str, content: str, memory_type: MemoryType = MemoryType.FACT, conversation_id: str = "harness-123", **kwargs):
        obj_in = MemoryCreate(
            title=title,
            content=content,
            conversation_id=conversation_id,
            memory_type=memory_type,
            **kwargs
        )
        return await self._execute(memory_service.create_memory, self.user_id, obj_in)

    async def update_memory(self, mem_id: str, **update_data):
        obj_in = MemoryUpdate(**update_data)
        return await self._execute(memory_service.update_memory, self.user_id, mem_id, obj_in)

    async def retrieve_memory(self, query: str, top_k: int = 5, conversation_id: str = "harness-123"):
        obj_in = RetrievalQuery(
            query=query,
            top_k=top_k,
            conversation_id=conversation_id
        )
        return await self._execute(retrieval_service.semantic_search, self.user_id, obj_in)

    async def create_conversation(self, title: str = "Attack Harness Test"):
        obj_in = ConversationCreate(title=title)
        return await self._execute(chat_service.create_conversation, self.user_id, obj_in)

    async def send_message(self, conv_id: str, content: str):
        obj_in = MessageCreate(content=content, role=MessageRole.USER)
        return await self._execute(chat_service.send_message, self.user_id, conv_id, obj_in)

    async def get_explanation(self, memory_id: str):
        from app.modules.explainability.service import explanation_service
        return await self._execute(explanation_service.get_explanation, memory_id)
