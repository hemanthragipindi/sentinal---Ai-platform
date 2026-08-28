from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from google.oauth2 import id_token
from google.auth.transport import requests
import uuid

from app.core.security import get_password_hash, verify_password, create_access_token, create_refresh_token, decode_token
from app.core.exceptions import SentinelException
from app.core.config import settings
from app.modules.auth.schemas import UserRegister, UserLogin, Token, UserCreateDB, UserResponse
from app.modules.auth.repository import user_repo, refresh_token_repo
from app.database.models.enums import UserStatus

class AuthService:
    async def register(self, db: AsyncSession, obj_in: UserRegister) -> UserResponse:
        # Check if email exists
        user = await user_repo.get_by_email(db, obj_in.email)
        if user:
            raise SentinelException("Email already registered", status_code=400)
            
        # Check if username exists
        user_by_username = await user_repo.get_by_username(db, obj_in.username)
        if user_by_username:
            raise SentinelException("Username already taken", status_code=400)
            
        create_data = UserCreateDB(
            email=obj_in.email,
            username=obj_in.username,
            password_hash=get_password_hash(obj_in.password),
            full_name=obj_in.full_name
        )
        
        db_user = await user_repo.create(db, create_data)
        await db.commit()
        return UserResponse.model_validate(db_user)

    async def login(self, db: AsyncSession, obj_in: UserLogin) -> Token:
        user = await user_repo.get_by_email(db, obj_in.email)
        if not user or not verify_password(obj_in.password, user.password_hash):
            if user:
                user.failed_login_attempts += 1
                await db.commit()
            raise SentinelException("Incorrect email or password", status_code=401)
            
        if user.status != UserStatus.ACTIVE or not user.is_active:
            raise SentinelException("User account is inactive or blocked", status_code=403)
            
        # Reset attempts and track login
        user.failed_login_attempts = 0
        user.last_login_at = datetime.now(timezone.utc)
        await db.flush()

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        # Store refresh token
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await refresh_token_repo.create(db, {
            "user_id": user.id,
            "token_hash": refresh_token, # Normally hash this for security, storing raw for MVP
            "expires_at": expires_at
        })
        
        await db.commit()
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def google_login(self, db: AsyncSession, credential: str) -> Token:
        if not settings.GOOGLE_CLIENT_ID:
            raise SentinelException("Google Client ID not configured", status_code=500)
            
        try:
            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                credential, 
                requests.Request(), 
                settings.GOOGLE_CLIENT_ID,
                clock_skew_in_seconds=10
            )
        except ValueError:
            raise SentinelException("Invalid Google token", status_code=401)
            
        email = idinfo.get('email')
        if not email:
            raise SentinelException("Email not provided by Google", status_code=400)
            
        user = await user_repo.get_by_email(db, email)
        
        # If user doesn't exist, create them
        if not user:
            # Generate a random password since they use Google
            random_password = str(uuid.uuid4())
            # Generate a username from email if possible
            base_username = email.split('@')[0]
            # Ensure unique username
            existing = await user_repo.get_by_username(db, base_username)
            username = f"{base_username}_{str(uuid.uuid4())[:8]}" if existing else base_username
            
            create_data = UserCreateDB(
                email=email,
                username=username,
                password_hash=get_password_hash(random_password),
                full_name=idinfo.get('name')
            )
            user = await user_repo.create(db, create_data)
            await db.commit()
            
        if user.status != UserStatus.ACTIVE or not user.is_active:
            raise SentinelException("User account is inactive or blocked", status_code=403)
            
        # Track login
        user.failed_login_attempts = 0
        user.last_login_at = datetime.now(timezone.utc)
        await db.flush()

        access_token = create_access_token(subject=user.id)
        refresh_token = create_refresh_token(subject=user.id)
        
        # Store refresh token
        expires_at = datetime.now(timezone.utc) + timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
        await refresh_token_repo.create(db, {
            "user_id": user.id,
            "token_hash": refresh_token,
            "expires_at": expires_at
        })
        
        await db.commit()
        return Token(access_token=access_token, refresh_token=refresh_token)
        
    async def refresh(self, db: AsyncSession, refresh_token: str) -> Token:
        payload = decode_token(refresh_token)
        if not payload or payload.get("type") != "refresh":
            raise SentinelException("Invalid refresh token", status_code=401)
            
        user_id = payload.get("sub")
        db_token = await refresh_token_repo.get_by_token(db, refresh_token)
        if not db_token or str(db_token.user_id) != user_id:
            raise SentinelException("Invalid refresh token", status_code=401)
            
        if db_token.expires_at < datetime.now(timezone.utc):
            raise SentinelException("Refresh token expired", status_code=401)
            
        user = await user_repo.get_by_id(db, user_id)
        if not user or not user.is_active:
            raise SentinelException("User inactive", status_code=401)
            
        access_token = create_access_token(subject=user.id)
        return Token(access_token=access_token, refresh_token=refresh_token)

    async def logout(self, db: AsyncSession, refresh_token: str) -> None:
        db_token = await refresh_token_repo.get_by_token(db, refresh_token)
        if db_token:
            await refresh_token_repo.soft_delete(db, db_token.id)
            await db.commit()

auth_service = AuthService()
