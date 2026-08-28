from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from app.core.database import get_db
from app.modules.explainability.schemas import ExplanationResult
from app.modules.explainability.service import explanation_service

router = APIRouter(prefix="/explain", tags=["Explainability"])

@router.get("/{memory_id}", response_model=ExplanationResult)
async def get_explanation(memory_id: str, db: AsyncSession = Depends(get_db)):
    return await explanation_service.get_explanation(db, memory_id)
