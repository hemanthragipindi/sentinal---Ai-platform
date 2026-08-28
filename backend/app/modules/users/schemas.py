from pydantic import BaseModel, HttpUrl
from typing import Optional

class UserUpdate(BaseModel):
    full_name: Optional[str] = None

class AvatarUpdate(BaseModel):
    avatar_url: HttpUrl
