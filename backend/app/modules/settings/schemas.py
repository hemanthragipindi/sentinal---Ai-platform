from pydantic import BaseModel, Field
from typing import Optional

class UserSettingsUpdate(BaseModel):
    theme: Optional[str] = None
    default_model: Optional[str] = None
    temperature: Optional[float] = Field(None, ge=0.0, le=2.0)
    top_p: Optional[float] = Field(None, ge=0.0, le=1.0)
    max_tokens: Optional[int] = Field(None, ge=1)

class UserSettingsResponse(BaseModel):
    id: str
    user_id: str
    theme: str
    default_model: str
    temperature: float
    top_p: float
    max_tokens: int
    
    class Config:
        from_attributes = True
