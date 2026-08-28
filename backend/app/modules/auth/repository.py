from typing import Any
from sqlalchemy import select, update, func
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.repository import BaseRepository
from app.modules.auth.models import User, RefreshToken, UserSession
from app.modules.auth.schemas import UserCreateDB

class UserRepository(BaseRepository[User, UserCreateDB, Any]):
    def __init__(self):
        super().__init__(User)
        
    async def get_by_email(self, db: AsyncSession, email: str) -> User | None:
        stmt = select(User).where(User.email == email, User.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first()

    async def get_by_username(self, db: AsyncSession, username: str) -> User | None:
        stmt = select(User).where(User.username == username, User.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first()

class RefreshTokenRepository(BaseRepository[RefreshToken, dict, Any]):
    def __init__(self):
        super().__init__(RefreshToken)
        
    async def get_by_token(self, db: AsyncSession, token_hash: str) -> RefreshToken | None:
        stmt = select(RefreshToken).where(RefreshToken.token_hash == token_hash, RefreshToken.deleted_at.is_(None))
        result = await db.execute(stmt)
        return result.scalars().first()
        
    async def delete_by_token(self, db: AsyncSession, token_hash: str) -> None:
        stmt = update(RefreshToken).where(RefreshToken.token_hash == token_hash).values(deleted_at=func.now())
        await db.execute(stmt)
        await db.flush()

class UserSessionRepository(BaseRepository[UserSession, dict, Any]):
    def __init__(self):
        super().__init__(UserSession)

user_repo = UserRepository()
refresh_token_repo = RefreshTokenRepository()
user_session_repo = UserSessionRepository()
