from typing import Any
from sqlalchemy.ext.asyncio import AsyncSession
from app.shared.repository import BaseRepository
from app.modules.threat_detection.models import AnomalyResult, QuarantinedMemory

class AnomalyResultRepository(BaseRepository[AnomalyResult, dict, Any]):
    def __init__(self):
        super().__init__(AnomalyResult)

class QuarantinedMemoryRepository(BaseRepository[QuarantinedMemory, dict, Any]):
    def __init__(self):
        super().__init__(QuarantinedMemory)

anomaly_result_repo = AnomalyResultRepository()
quarantined_memory_repo = QuarantinedMemoryRepository()
