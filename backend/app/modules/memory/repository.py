from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.memory.models import Memory, MemoryVersion, MemoryEmbedding, MemoryProvenance

class MemoryRepository(BaseRepository[Memory, dict, Any]):
    def __init__(self):
        super().__init__(Memory)

    async def list_by_user(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
        stmt = select(Memory).where(
            Memory.user_id == user_id, 
            Memory.deleted_at.is_(None)
        ).order_by(Memory.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

    async def get_by_id_with_provenance(self, db: AsyncSession, id: Any) -> Memory | None:
        from sqlalchemy.orm import selectinload
        stmt = select(Memory).options(selectinload(Memory.provenance)).where(Memory.id == id, Memory.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first()

class MemoryVersionRepository(BaseRepository[MemoryVersion, dict, Any]):
    def __init__(self):
        super().__init__(MemoryVersion)
        
class MemoryEmbeddingRepository(BaseRepository[MemoryEmbedding, dict, Any]):
    def __init__(self):
        super().__init__(MemoryEmbedding)

class MemoryProvenanceRepository(BaseRepository[MemoryProvenance, dict, Any]):
    def __init__(self):
        super().__init__(MemoryProvenance)

memory_repo = MemoryRepository()
memory_version_repo = MemoryVersionRepository()
memory_embedding_repo = MemoryEmbeddingRepository()
memory_provenance_repo = MemoryProvenanceRepository()
