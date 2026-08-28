from pydantic import BaseModel
from typing import Optional, Dict, Any

class AnomalyResultResponse(BaseModel):
    id: str
    memory_id: str
    memory_version: int
    score: float
    is_suspicious: bool
    signals: Optional[Dict[str, Any]] = None

    class Config:
        from_attributes = True
