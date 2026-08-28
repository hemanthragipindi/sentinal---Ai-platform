from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.shared.dependencies import get_current_superuser, pagination_params
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.jobs.schemas import JobCreate, JobResponse, JobLogResponse
from app.modules.jobs.service import job_service
from app.modules.jobs.repository import job_repo, job_log_repo

router = APIRouter(prefix="/jobs", tags=["Background Jobs"])

@router.post("", response_model=StandardResponse[JobResponse])
async def create_job(
    job_in: JobCreate,
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser)
):
    job = await job_service.create_job(db, job_in)
    return success_response(data=JobResponse.model_validate(job))

@router.get("", response_model=StandardResponse[List[JobResponse]])
async def list_jobs(
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser),
    pagination: dict = Depends(pagination_params)
):
    jobs = await job_repo.list_all(db, skip=pagination["skip"], limit=pagination["limit"])
    data = [JobResponse.model_validate(j) for j in jobs]
    return success_response(data=data)

@router.get("/{job_id}", response_model=StandardResponse[JobResponse])
async def get_job(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser)
):
    job = await job_service.get_job(db, job_id)
    return success_response(data=JobResponse.model_validate(job))

@router.get("/{job_id}/logs", response_model=StandardResponse[List[JobLogResponse]])
async def get_job_logs(
    job_id: str,
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser),
    pagination: dict = Depends(pagination_params)
):
    await job_service.get_job(db, job_id) # Verify exists
    logs = await job_log_repo.list_by_job(db, job_id, skip=pagination["skip"], limit=pagination["limit"])
    data = [JobLogResponse.model_validate(l) for l in logs]
    return success_response(data=data)
