from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging

from app.modules.memory.models import MemoryVersion
from app.modules.memory.service import memory_service
from app.modules.memory.schemas import MemoryUpdate
from app.modules.threat_detection.repository import quarantined_memory_repo
from app.modules.threat_detection.models import QuarantinedMemory
from app.database.models.enums import MemoryStatus
from app.core.exceptions import SentinelException

logger = logging.getLogger(__name__)

class RollbackService:
    async def rollback_memory(self, db: AsyncSession, user_id: str, memory_id: str, target_version: int) -> dict:
        """
        Restores a previous trusted memory version while preserving the complete history of the action.
        """
        # Fetch the target version
        stmt = select(MemoryVersion).where(
            MemoryVersion.memory_id == memory_id,
            MemoryVersion.version == target_version
        )
        result = await db.execute(stmt)
        old_version = result.scalars().first()
        
        if not old_version:
            raise SentinelException(f"Version {target_version} not found for memory {memory_id}", status_code=404)
            
        # We perform a standard update with the old content.
        # This will create a NEW version, generate a new embedding, and run the anomaly check.
        # It preserves history because the poisoned version is not deleted.
        update_data = MemoryUpdate(content=old_version.content)
        
        # update_memory will run the Anomaly Detection check. If safe, it might not quarantine it.
        # However, we should explicitly un-quarantine it if it passed the check.
        # Wait, if update_memory is called, it might get quarantined again if the anomaly detector flags it.
        # If it doesn't get flagged, we must ensure it is ACTIVE.
        
        updated_memory = await memory_service.update_memory(db, user_id, memory_id, update_data)
        
        # If the newly generated version is not quarantined by the anomaly detector,
        # we make sure it's active and clean up the quarantine status.
        if updated_memory.status != MemoryStatus.QUARANTINED:
            updated_memory.status = MemoryStatus.ACTIVE
            
            # Update the QuarantinedMemory record if it exists
            q_stmt = select(QuarantinedMemory).where(
                QuarantinedMemory.memory_id == memory_id,
                QuarantinedMemory.status == "active"
            )
            q_result = await db.execute(q_stmt)
            q_record = q_result.scalars().first()
            
            if q_record:
                q_record.status = "rolled_back"
                
        await db.commit()
        return updated_memory

rollback_service = RollbackService()
