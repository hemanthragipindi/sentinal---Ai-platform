from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.shared.repository import BaseRepository
from app.modules.settings.models import UserSettings

class UserSettingsRepository(BaseRepository[UserSettings, dict, Any]):
    def __init__(self):
        super().__init__(UserSettings)
        
    async def get_by_user(self, db: AsyncSession, user_id: str) -> UserSettings | None:
        stmt = select(UserSettings).where(
            UserSettings.user_id == user_id, 
            UserSettings.deleted_at.is_(None)
        )
        result = await db.execute(stmt)
        return result.scalars().first()

user_settings_repo = UserSettingsRepository()
