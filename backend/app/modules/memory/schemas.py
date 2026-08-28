from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional
from app.database.models.enums import MemoryType, MemoryStatus

class MemoryCreate(BaseModel):
    conversation_id: str
    title: str = Field(..., max_length=255)
    content: str
    summary: Optional[str] = None
    memory_type: MemoryType = MemoryType.FACT
    importance_score: float = Field(default=0.5, ge=0.0, le=1.0)
    confidence_score: float = Field(default=0.5, ge=0.0, le=1.0)
    trust_score: float = Field(default=0.5, ge=0.0, le=1.0)
    source: Optional[str] = None
    source_type: str = "SYSTEM"

class MemoryUpdate(BaseModel):
    title: Optional[str] = Field(None, max_length=255)
    content: Optional[str] = None
    summary: Optional[str] = None
    importance_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    confidence_score: Optional[float] = Field(None, ge=0.0, le=1.0)
    trust_score: Optional[float] = Field(None, ge=0.0, le=1.0)

class MemoryProvenanceResponse(BaseModel):
    id: str
    source_type: str
    original_content_hash: str
    
    class Config:
        from_attributes = True

class MemoryResponse(BaseModel):
    id: str
    user_id: str
    conversation_id: str
    title: str
    content: str
    summary: Optional[str]
    memory_type: MemoryType
    importance_score: float
    confidence_score: float
    trust_score: float
    status: MemoryStatus
    embedding_status: str
    source: Optional[str]
    created_at: datetime
    version: int
    provenance: Optional[MemoryProvenanceResponse] = None
    has_changed: Optional[bool] = None
    
    class Config:
        from_attributes = True

