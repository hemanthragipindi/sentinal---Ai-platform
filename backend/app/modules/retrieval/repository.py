from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.memory.models import RetrievalLog, RetrievedMemory

class RetrievalLogRepository(BaseRepository[RetrievalLog, dict, Any]):
    def __init__(self):
        super().__init__(RetrievalLog)

class RetrievedMemoryRepository(BaseRepository[RetrievedMemory, dict, Any]):
    def __init__(self):
        super().__init__(RetrievedMemory)

retrieval_log_repo = RetrievalLogRepository()
retrieved_memory_repo = RetrievedMemoryRepository()
