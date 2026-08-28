from pydantic import BaseModel, EmailStr, Field
from datetime import datetime
from app.database.models.enums import UserStatus

class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str = "bearer"

class UserRegister(BaseModel):
    email: EmailStr
    username: str = Field(..., min_length=3, max_length=50)
    password: str = Field(..., min_length=8)
    full_name: str | None = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GoogleLoginRequest(BaseModel):
    credential: str

class RefreshTokenRequest(BaseModel):
    refresh_token: str

class UserResponse(BaseModel):
    id: str
    email: str
    username: str
    full_name: str | None
    status: UserStatus
    is_active: bool
    created_at: datetime
    
    class Config:
        from_attributes = True

class UserCreateDB(BaseModel):
    email: str
    username: str
    password_hash: str
    full_name: str | None
