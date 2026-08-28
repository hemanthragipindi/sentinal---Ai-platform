from sqlalchemy.ext.asyncio import AsyncSession
import logging

from app.modules.memory.models import Memory
from app.modules.memory.repository import memory_repo
from app.modules.threat_detection.models import AnomalyResult
from app.modules.threat_detection.repository import quarantined_memory_repo
from app.database.models.enums import MemoryStatus

logger = logging.getLogger(__name__)

class QuarantineService:
    def __init__(self):
        # Configuration for automated quarantine
        self.auto_quarantine_enabled = True

    async def evaluate_and_quarantine(self, db: AsyncSession, memory: Memory, anomaly_result: AnomalyResult) -> None:
        """
        Policy-based evaluation. In the research/demo environment, automatically
        quarantine if suspicious, but keep the decision in this dedicated service.
        """
        if self.auto_quarantine_enabled and anomaly_result.is_suspicious:
            await self.quarantine_memory(
                db, 
                memory, 
                reason=f"Automatically quarantined due to high anomaly score ({anomaly_result.score:.2f})"
            )

    async def quarantine_memory(self, db: AsyncSession, memory: Memory, reason: str) -> None:
        """
        Execute the quarantine action: change memory status and record the event.
        """
        if memory.status == MemoryStatus.QUARANTINED:
            return # Already quarantined
            
        memory.status = MemoryStatus.QUARANTINED
        await memory_repo.update(db, memory, {"status": MemoryStatus.QUARANTINED})
        
        await quarantined_memory_repo.create(db, {
            "memory_id": memory.id,
            "reason": reason,
            "status": "active"
        })
        
        logger.info(f"Memory {memory.id} quarantined. Reason: {reason}")
        await db.commit()

quarantine_service = QuarantineService()
