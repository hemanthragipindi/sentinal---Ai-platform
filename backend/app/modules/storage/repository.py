from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.storage.models import File, FileAccessLog

class FileRepository(BaseRepository[File, dict, Any]):
    def __init__(self):
        super().__init__(File)
        
    async def list_by_user(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
        stmt = select(File).where(
            File.user_id == user_id, 
            File.deleted_at.is_(None)
        ).order_by(File.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

class FileAccessLogRepository(BaseRepository[FileAccessLog, dict, Any]):
    def __init__(self):
        super().__init__(FileAccessLog)

file_repo = FileRepository()
file_access_log_repo = FileAccessLogRepository()
