from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.jobs.models import Job, JobLog

class JobRepository(BaseRepository[Job, dict, Any]):
    def __init__(self):
        super().__init__(Job)
        
    async def list_all(self, db: AsyncSession, skip: int = 0, limit: int = 100):
        stmt = select(Job).where(Job.deleted_at.is_(None)).order_by(Job.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

class JobLogRepository(BaseRepository[JobLog, dict, Any]):
    def __init__(self):
        super().__init__(JobLog)
        
    async def list_by_job(self, db: AsyncSession, job_id: str, skip: int = 0, limit: int = 100):
        stmt = select(JobLog).where(
            JobLog.job_id == job_id, 
            JobLog.deleted_at.is_(None)
        ).order_by(JobLog.created_at.desc()).offset(skip).limit(limit)
        result = await db.execute(stmt)
        return result.scalars().all()

job_repo = JobRepository()
job_log_repo = JobLogRepository()
