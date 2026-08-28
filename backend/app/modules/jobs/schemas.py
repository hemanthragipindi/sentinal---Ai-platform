from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
from app.database.models.enums import JobStatus

class JobCreate(BaseModel):
    name: str
    payload: Optional[dict[str, Any]] = None

class JobResponse(BaseModel):
    id: str
    name: str
    status: JobStatus
    payload: Optional[dict[str, Any]]
    started_at: Optional[datetime]
    completed_at: Optional[datetime]
    retry_count: int
    error_message: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class JobLogResponse(BaseModel):
    id: str
    job_id: str
    message: str
    level: str
    created_at: datetime
    
    class Config:
        from_attributes = True
