from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.modules.jobs.repository import job_repo
from app.modules.jobs.schemas import JobCreate
from app.modules.jobs.models import Job
from app.core.exceptions import SentinelException
from app.database.models.enums import JobStatus

class JobService:
    async def create_job(self, db: AsyncSession, obj_in: JobCreate) -> Job:
        data = obj_in.model_dump()
        data["status"] = JobStatus.PENDING
        
        job = await job_repo.create(db, data)
        await db.commit()
        return job

    async def get_job(self, db: AsyncSession, job_id: str) -> Job:
        job = await job_repo.get_by_id(db, job_id)
        if not job:
            raise SentinelException("Job not found", status_code=404)
        return job

    async def update_job_status(self, db: AsyncSession, job_id: str, status: JobStatus) -> Job:
        job = await self.get_job(db, job_id)
        
        update_data = {"status": status}
        if status == JobStatus.RUNNING:
            update_data["started_at"] = datetime.now(timezone.utc)
        elif status in [JobStatus.COMPLETED, JobStatus.FAILED, JobStatus.CANCELLED]:
            update_data["completed_at"] = datetime.now(timezone.utc)
            
        updated_job = await job_repo.update(db, job, update_data)
        await db.commit()
        return updated_job

job_service = JobService()
