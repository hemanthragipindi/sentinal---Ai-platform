from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime
from app.database.models.enums import ReportStatus

class ReportCreate(BaseModel):
    title: str
    report_type: str
    content: dict[str, Any]

class ReportResponse(BaseModel):
    id: str
    user_id: str
    title: str
    report_type: str
    content: dict[str, Any]
    status: ReportStatus
    download_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True
