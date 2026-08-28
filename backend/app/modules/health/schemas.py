from pydantic import BaseModel

class HealthResponse(BaseModel):
    version: str
    timestamp: str
    status: str
    database: dict
    pgvector: dict
    supabase: dict
    huggingface: dict
