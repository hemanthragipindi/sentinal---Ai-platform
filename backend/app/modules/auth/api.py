from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.modules.auth.schemas import UserRegister, UserLogin, GoogleLoginRequest, RefreshTokenRequest, Token, UserResponse
from app.modules.auth.service import auth_service
from app.shared.schemas import StandardResponse, success_response

router = APIRouter(prefix="/auth", tags=["Authentication"])

@router.post("/register", response_model=StandardResponse[UserResponse])
async def register(user_in: UserRegister, db: AsyncSession = Depends(get_db)):
    user = await auth_service.register(db, user_in)
    return success_response(data=user, message="User registered successfully")

@router.post("/login", response_model=StandardResponse[Token])
async def login(login_in: UserLogin, db: AsyncSession = Depends(get_db)):
    token = await auth_service.login(db, login_in)
    return success_response(data=token, message="Login successful")

@router.post("/google", response_model=StandardResponse[Token])
async def google_login(login_in: GoogleLoginRequest, db: AsyncSession = Depends(get_db)):
    token = await auth_service.google_login(db, login_in.credential)
    return success_response(data=token, message="Google login successful")

@router.post("/refresh", response_model=StandardResponse[Token])
async def refresh_token(token_in: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    token = await auth_service.refresh(db, token_in.refresh_token)
    return success_response(data=token, message="Token refreshed successfully")

@router.post("/logout", response_model=StandardResponse[None])
async def logout(token_in: RefreshTokenRequest, db: AsyncSession = Depends(get_db)):
    await auth_service.logout(db, token_in.refresh_token)
    return success_response(message="Logged out successfully")
