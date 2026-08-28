from pydantic import BaseModel
from datetime import datetime
from app.database.models.enums import ConversationStatus, MessageRole
from typing import Optional

class ConversationCreate(BaseModel):
    title: str = "New Conversation"
    model_name: str = "gpt-4"

class ConversationUpdate(BaseModel):
    title: Optional[str] = None
    status: Optional[ConversationStatus] = None

class ConversationResponse(BaseModel):
    id: str
    title: str
    model_name: str
    status: ConversationStatus
    total_tokens: int
    message_count: int
    last_message_at: Optional[datetime]
    created_at: datetime
    
    class Config:
        from_attributes = True

class MessageCreate(BaseModel):
    content: str
    role: MessageRole

class MessageResponse(BaseModel):
    id: str
    conversation_id: str
    role: MessageRole
    content: str
    finish_reason: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
