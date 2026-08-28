from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.settings.repository import user_settings_repo
from app.modules.settings.schemas import UserSettingsUpdate
from app.modules.settings.models import UserSettings

class SettingsService:
    async def get_or_create_user_settings(self, db: AsyncSession, user_id: str) -> UserSettings:
        settings = await user_settings_repo.get_by_user(db, user_id)
        if not settings:
            settings = await user_settings_repo.create(db, {"user_id": user_id})
            await db.commit()
        return settings

    async def update_user_settings(self, db: AsyncSession, user_id: str, obj_in: UserSettingsUpdate) -> UserSettings:
        settings = await self.get_or_create_user_settings(db, user_id)
        update_data = obj_in.model_dump(exclude_unset=True)
        
        updated_settings = await user_settings_repo.update(db, settings, update_data)
        await db.commit()
        return updated_settings

settings_service = SettingsService()
