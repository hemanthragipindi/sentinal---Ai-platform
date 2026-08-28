from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.audit.models import AuditLog

class AuditLogRepository(BaseRepository[AuditLog, dict, Any]):
    def __init__(self):
        super().__init__(AuditLog)
        
    async def list_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        # Admin or restricted access
        stmt = select(AuditLog).order_by(AuditLog.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

audit_log_repo = AuditLogRepository()
