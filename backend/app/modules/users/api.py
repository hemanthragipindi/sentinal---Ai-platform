from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.modules.auth.models import User
from app.modules.auth.schemas import UserResponse
from app.modules.users.schemas import UserUpdate, AvatarUpdate
from app.modules.users.service import user_service
from app.shared.schemas import StandardResponse, success_response

router = APIRouter(prefix="/users", tags=["Users"])

@router.get("/me", response_model=StandardResponse[UserResponse])
async def get_me(current_user: User = Depends(get_current_user)):
    return success_response(data=UserResponse.model_validate(current_user))

@router.patch("/me", response_model=StandardResponse[UserResponse])
async def update_me(
    update_in: UserUpdate, 
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    user = await user_service.update_profile(db, current_user, update_in)
    return success_response(data=user, message="Profile updated successfully")

@router.patch("/me/avatar", response_model=StandardResponse[UserResponse])
async def update_avatar(
    avatar_in: AvatarUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    # Pass as dictionary since it's an HttpUrl object
    user = await user_service.update_profile(db, current_user, {"avatar_url": str(avatar_in.avatar_url)})
    return success_response(data=user, message="Avatar updated successfully")

@router.delete("/me", response_model=StandardResponse[None])
async def delete_me(
    db: AsyncSession = Depends(get_db), 
    current_user: User = Depends(get_current_user)
):
    await user_service.soft_delete(db, current_user)
    return success_response(message="Account deleted successfully")
