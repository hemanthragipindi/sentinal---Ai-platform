from sqlalchemy.ext.asyncio import AsyncSession
from app.modules.auth.schemas import UserResponse
from app.modules.users.schemas import UserUpdate
from app.modules.auth.repository import user_repo
from app.modules.auth.models import User

class UserService:
    async def update_profile(self, db: AsyncSession, current_user: User, update_in: UserUpdate | dict) -> UserResponse:
        update_data = update_in if isinstance(update_in, dict) else update_in.model_dump(exclude_unset=True)
        updated_user = await user_repo.update(db, current_user, update_data)
        return UserResponse.model_validate(updated_user)
        
    async def soft_delete(self, db: AsyncSession, current_user: User) -> None:
        await user_repo.soft_delete(db, current_user.id)
        await db.commit()

user_service = UserService()
