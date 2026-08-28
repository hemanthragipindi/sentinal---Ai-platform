from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.settings.schemas import UserSettingsUpdate, UserSettingsResponse
from app.modules.settings.service import settings_service

router = APIRouter(prefix="/settings", tags=["Settings"])

@router.get("", response_model=StandardResponse[UserSettingsResponse])
async def get_settings(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sett = await settings_service.get_or_create_user_settings(db, str(current_user.id))
    return success_response(data=UserSettingsResponse.model_validate(sett))

@router.patch("", response_model=StandardResponse[UserSettingsResponse])
async def update_settings(
    settings_in: UserSettingsUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    sett = await settings_service.update_user_settings(db, str(current_user.id), settings_in)
    return success_response(data=UserSettingsResponse.model_validate(sett))
