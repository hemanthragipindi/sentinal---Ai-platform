from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.reports.models import Report

class ReportRepository(BaseRepository[Report, dict, Any]):
    def __init__(self):
        super().__init__(Report)
        
    async def list_by_user(self, db: AsyncSession, user_id: str, skip: int = 0, limit: int = 100):
        stmt = select(Report).where(
            Report.user_id == user_id, 
            Report.deleted_at.is_(None)
        ).order_by(Report.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

report_repo = ReportRepository()
