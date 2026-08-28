from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.shared.dependencies import get_current_user, pagination_params
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.reports.schemas import ReportCreate, ReportResponse
from app.modules.reports.service import report_service
from app.modules.reports.repository import report_repo

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.post("", response_model=StandardResponse[ReportResponse])
async def create_report(
    report_in: ReportCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rep = await report_service.create_report(db, str(current_user.id), report_in)
    return success_response(data=ReportResponse.model_validate(rep))

@router.get("", response_model=StandardResponse[List[ReportResponse]])
async def list_reports(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination_params)
):
    reps = await report_repo.list_by_user(db, str(current_user.id), skip=pagination["skip"], limit=pagination["limit"])
    data = [ReportResponse.model_validate(r) for r in reps]
    return success_response(data=data)

@router.get("/{report_id}", response_model=StandardResponse[ReportResponse])
async def get_report(
    report_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    rep = await report_service.get_report(db, str(current_user.id), report_id)
    return success_response(data=ReportResponse.model_validate(rep))
