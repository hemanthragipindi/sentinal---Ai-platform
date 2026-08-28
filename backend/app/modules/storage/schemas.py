from pydantic import BaseModel, HttpUrl
from typing import Optional
from datetime import datetime
from app.database.models.enums import FileAccessAction

class FileMetadataCreate(BaseModel):
    bucket: str
    file_name: str
    storage_path: str
    mime_type: str
    file_size: int
    public_url: Optional[HttpUrl] = None

class FileMetadataResponse(BaseModel):
    id: str
    user_id: str
    bucket: str
    file_name: str
    storage_path: str
    mime_type: str
    file_size: int
    public_url: Optional[str]
    created_at: datetime
    
    class Config:
        from_attributes = True

class FileUploadResponse(BaseModel):
    file: FileMetadataResponse
    upload_url: str # Pre-signed URL for client to upload to Supabase

class FileDownloadResponse(BaseModel):
    download_url: str # Pre-signed URL for client to download
