from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.shared.dependencies import get_current_user, pagination_params
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.memory.schemas import MemoryCreate, MemoryUpdate, MemoryResponse
from app.modules.memory.service import memory_service
from app.modules.memory.repository import memory_repo

router = APIRouter(prefix="/memory", tags=["Memory"])

@router.post("", response_model=StandardResponse[MemoryResponse])
async def create_memory(
    mem_in: MemoryCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mem = await memory_service.create_memory(db, str(current_user.id), mem_in)
    return success_response(data=MemoryResponse.model_validate(mem))

@router.get("", response_model=StandardResponse[List[MemoryResponse]])
async def list_memories(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination_params)
):
    mems = await memory_repo.list_by_user(db, str(current_user.id), skip=pagination["skip"], limit=pagination["limit"])
    data = [MemoryResponse.model_validate(m) for m in mems]
    return success_response(data=data)

@router.get("/{mem_id}", response_model=StandardResponse[MemoryResponse])
async def get_memory(
    mem_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mem = await memory_service.get_memory(db, str(current_user.id), mem_id)
    return success_response(data=MemoryResponse.model_validate(mem))

@router.patch("/{mem_id}", response_model=StandardResponse[MemoryResponse])
async def update_memory(
    mem_id: str,
    mem_in: MemoryUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    mem = await memory_service.update_memory(db, str(current_user.id), mem_id, mem_in)
    return success_response(data=MemoryResponse.model_validate(mem))

@router.delete("/{mem_id}", response_model=StandardResponse[None])
async def delete_memory(
    mem_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await memory_service.delete_memory(db, str(current_user.id), mem_id)
    return success_response(message="Memory deleted")
