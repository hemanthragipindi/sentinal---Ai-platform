from pydantic import BaseModel
from typing import Any, Optional
from datetime import datetime

class AuditLogResponse(BaseModel):
    id: str
    user_id: Optional[str]
    action: str
    entity: str
    entity_id: Optional[str]
    metadata_data: Optional[dict[str, Any]]
    created_at: datetime
    
    class Config:
        from_attributes = True
