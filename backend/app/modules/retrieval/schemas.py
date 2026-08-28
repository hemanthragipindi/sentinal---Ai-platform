from pydantic import BaseModel, Field
from typing import List, Optional
from datetime import datetime
from app.modules.memory.schemas import MemoryResponse

class RetrievalQuery(BaseModel):
    query: str
    conversation_id: str
    top_k: int = Field(5, ge=1, le=20)
    min_score: float = Field(0.7, ge=0.0, le=1.0)

class RetrievedMemoryResult(BaseModel):
    memory: MemoryResponse
    similarity_score: float
    rank: int

class RetrievalResponse(BaseModel):
    query: str
    top_k: int
    response_time: float
    results: List[RetrievedMemoryResult]
    
    class Config:
        from_attributes = True
