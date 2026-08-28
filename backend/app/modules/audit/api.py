from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.shared.dependencies import get_current_superuser, pagination_params
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.audit.schemas import AuditLogResponse
from app.modules.audit.service import audit_service
from app.modules.audit.repository import audit_log_repo

router = APIRouter(prefix="/audit", tags=["Audit"])

@router.get("", response_model=StandardResponse[List[AuditLogResponse]])
async def list_logs(
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser),
    pagination: dict = Depends(pagination_params)
):
    logs = await audit_log_repo.list_all(db, skip=pagination["skip"], limit=pagination["limit"])
    data = [AuditLogResponse.model_validate(l) for l in logs]
    return success_response(data=data)

@router.get("/{log_id}", response_model=StandardResponse[AuditLogResponse])
async def get_log(
    log_id: str,
    db: AsyncSession = Depends(get_db),
    current_superuser: User = Depends(get_current_superuser)
):
    log = await audit_service.get_audit_log(db, log_id)
    return success_response(data=AuditLogResponse.model_validate(log))
