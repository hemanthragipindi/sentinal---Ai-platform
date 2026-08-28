from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from typing import List

from app.core.database import get_db
from app.shared.dependencies import get_current_user, pagination_params
from app.shared.schemas import StandardResponse, success_response, PaginatedResponse
from app.modules.auth.models import User
from app.modules.chat.schemas import ConversationCreate, ConversationUpdate, ConversationResponse, MessageCreate, MessageResponse
from app.modules.chat.service import chat_service
from app.modules.chat.repository import conversation_repo, message_repo

router = APIRouter(prefix="/chat", tags=["Chat"])

@router.post("/conversations", response_model=StandardResponse[ConversationResponse])
async def create_conversation(
    conv_in: ConversationCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = await chat_service.create_conversation(db, str(current_user.id), conv_in)
    return success_response(data=ConversationResponse.model_validate(conv))

@router.get("/conversations", response_model=StandardResponse[List[ConversationResponse]])
async def list_conversations(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination_params)
):
    convs = await conversation_repo.list_by_user(db, str(current_user.id), skip=pagination["skip"], limit=pagination["limit"])
    data = [ConversationResponse.model_validate(c) for c in convs]
    return success_response(data=data)

@router.get("/conversations/{conv_id}", response_model=StandardResponse[ConversationResponse])
async def get_conversation(
    conv_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = await chat_service.get_conversation(db, str(current_user.id), conv_id)
    return success_response(data=ConversationResponse.model_validate(conv))

@router.patch("/conversations/{conv_id}", response_model=StandardResponse[ConversationResponse])
async def update_conversation(
    conv_id: str,
    update_in: ConversationUpdate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    conv = await chat_service.update_conversation(db, str(current_user.id), conv_id, update_in)
    return success_response(data=ConversationResponse.model_validate(conv))

@router.delete("/conversations/{conv_id}", response_model=StandardResponse[None])
async def delete_conversation(
    conv_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    await chat_service.delete_conversation(db, str(current_user.id), conv_id)
    return success_response(message="Conversation deleted")

@router.post("/messages/{conv_id}", response_model=StandardResponse[MessageResponse])
async def send_message(
    conv_id: str,
    msg_in: MessageCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    msg = await chat_service.send_message(db, str(current_user.id), conv_id, msg_in)
    return success_response(data=MessageResponse.model_validate(msg))

@router.get("/messages/{conv_id}", response_model=StandardResponse[List[MessageResponse]])
async def list_messages(
    conv_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user),
    pagination: dict = Depends(pagination_params)
):
    await chat_service.get_conversation(db, str(current_user.id), conv_id) # Access check
    msgs = await message_repo.list_by_conversation(db, conv_id, skip=pagination["skip"], limit=pagination["limit"])
    data = [MessageResponse.model_validate(m) for m in msgs]
    return success_response(data=data)
