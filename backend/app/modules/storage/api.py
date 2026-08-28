from fastapi import APIRouter, Depends, Request
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db
from app.shared.dependencies import get_current_user
from app.shared.schemas import StandardResponse, success_response
from app.modules.auth.models import User
from app.modules.storage.schemas import FileMetadataCreate, FileUploadResponse, FileMetadataResponse, FileDownloadResponse
from app.modules.storage.service import storage_service

router = APIRouter(prefix="/storage", tags=["Storage"])

@router.post("/upload", response_model=StandardResponse[FileUploadResponse])
async def init_upload(
    file_in: FileMetadataCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    upload_info = await storage_service.initialize_upload(db, str(current_user.id), file_in)
    return success_response(data=upload_info, message="Upload initialized")

@router.get("/{file_id}", response_model=StandardResponse[FileMetadataResponse])
async def get_metadata(
    file_id: str,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    metadata = await storage_service.get_file_metadata(db, str(current_user.id), file_id)
    return success_response(data=FileMetadataResponse.model_validate(metadata))

@router.get("/{file_id}/download", response_model=StandardResponse[FileDownloadResponse])
async def get_download_url(
    file_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip_addr = request.client.host if request.client else "0.0.0.0"
    url_info = await storage_service.get_download_url(db, str(current_user.id), file_id, ip_addr)
    return success_response(data=url_info)

@router.delete("/{file_id}", response_model=StandardResponse[None])
async def delete_file(
    file_id: str,
    request: Request,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_current_user)
):
    ip_addr = request.client.host if request.client else "0.0.0.0"
    await storage_service.delete_file(db, str(current_user.id), file_id, ip_addr)
    return success_response(message="File deleted")
