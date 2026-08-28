from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.retrieval.schemas import RetrievalQuery, RetrievalResponse
from app.modules.retrieval.service import retrieval_service

router = APIRouter(prefix="/retrieval", tags=["Retrieval"])

@router.post("/search", response_model=StandardResponse[RetrievalResponse])
async def search_memories(
    query_in: RetrievalQuery,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    results = await retrieval_service.semantic_search(db, str(current_user.id), query_in)
    return success_response(data=results, message="Search completed")
