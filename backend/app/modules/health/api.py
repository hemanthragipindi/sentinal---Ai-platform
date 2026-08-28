from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.health.service import health_service
from app.shared.schemas import StandardResponse, success_response

router = APIRouter(prefix="/health", tags=["System Health"])

@router.get("", response_model=StandardResponse[dict])
async def get_health(db: AsyncSession = Depends(get_db)):
    health_data = await health_service.check_health(db)
    return success_response(data=health_data, message="System Health Check")
