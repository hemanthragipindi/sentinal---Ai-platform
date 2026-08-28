from sqlalchemy.ext.asyncio import AsyncSession
import uuid

from app.modules.storage.repository import file_repo, file_access_log_repo
from app.modules.storage.schemas import FileMetadataCreate, FileUploadResponse, FileDownloadResponse
from app.modules.storage.models import File
from app.storage.providers.supabase import supabase_client
from app.core.exceptions import SentinelException
from app.database.models.enums import FileAccessAction

class StorageService:
    async def initialize_upload(self, db: AsyncSession, user_id: str, file_in: FileMetadataCreate) -> FileUploadResponse:
        data = file_in.model_dump()
        data["user_id"] = user_id
        
        # Save metadata to DB
        db_file = await file_repo.create(db, data)
        await db.commit()
        
        # Generate signed upload URL from Supabase if client exists
        upload_url = ""
        client = supabase_client.get_client()
        if client:
            try:
                res = client.storage.from_(file_in.bucket).create_signed_upload_url(file_in.storage_path)
                upload_url = res.get('signedUrl', '')
            except Exception as e:
                # Fallback or log error
                pass
                
        return FileUploadResponse(
            file=db_file,
            upload_url=upload_url
        )

    async def get_file_metadata(self, db: AsyncSession, user_id: str, file_id: str) -> File:
        db_file = await file_repo.get_by_id(db, file_id)
        if not db_file or str(db_file.user_id) != str(user_id):
            raise SentinelException("File not found", status_code=404)
        return db_file

    async def get_download_url(self, db: AsyncSession, user_id: str, file_id: str, ip_address: str = "0.0.0.0") -> FileDownloadResponse:
        db_file = await self.get_file_metadata(db, user_id, file_id)
        
        # Log access
        await file_access_log_repo.create(db, {
            "file_id": db_file.id,
            "user_id": user_id,
            "action": FileAccessAction.DOWNLOAD,
            "ip_address": ip_address
        })
        await db.commit()
        
        download_url = db_file.public_url or ""
        client = supabase_client.get_client()
        if client and not download_url:
            try:
                # Generate 1 hour signed URL
                download_url = client.storage.from_(db_file.bucket).create_signed_url(db_file.storage_path, 3600)
            except:
                pass
                
        return FileDownloadResponse(download_url=download_url)

    async def delete_file(self, db: AsyncSession, user_id: str, file_id: str, ip_address: str = "0.0.0.0") -> None:
        db_file = await self.get_file_metadata(db, user_id, file_id)
        
        client = supabase_client.get_client()
        if client:
            try:
                client.storage.from_(db_file.bucket).remove([db_file.storage_path])
            except:
                pass
                
        await file_repo.soft_delete(db, db_file.id)
        
        # Log deletion
        await file_access_log_repo.create(db, {
            "file_id": db_file.id,
            "user_id": user_id,
            "action": FileAccessAction.DELETE,
            "ip_address": ip_address
        })
        await db.commit()

storage_service = StorageService()
