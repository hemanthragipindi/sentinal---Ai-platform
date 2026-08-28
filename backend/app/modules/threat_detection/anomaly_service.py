from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
import math
import numpy as np

from app.modules.threat_detection.models import AnomalyResult
from app.modules.threat_detection.repository import anomaly_result_repo
from app.modules.memory.models import Memory, MemoryEmbedding

logger = logging.getLogger(__name__)

def cosine_similarity(vec1: list[float], vec2: list[float]) -> float:
    # Handle both raw lists and numpy arrays
    v1 = np.array(vec1)
    v2 = np.array(vec2)
    
    # Calculate cosine similarity using numpy
    dot_product = np.dot(v1, v2)
    norm_v1 = np.linalg.norm(v1)
    norm_v2 = np.linalg.norm(v2)
    
    if norm_v1 == 0 or norm_v2 == 0:
        return 0.0
        
    return float(dot_product / (norm_v1 * norm_v2))

class AnomalyDetectionService:
    def __init__(self):
        self.THRESHOLD = 0.7

    async def analyze_memory(self, db: AsyncSession, memory: Memory, current_vector: list[float]) -> AnomalyResult:
        signals = {}
        drift_score = 0.0
        provenance_score = 0.0
        
        # 1. Provenance Signal
        source_type = "SYSTEM"
        if hasattr(memory, "provenance") and memory.provenance:
            source_type = memory.provenance.source_type
            
        if source_type == "SYSTEM":
            provenance_score = 0.0
        elif source_type == "USER":
            provenance_score = 0.2
        elif source_type == "API":
            provenance_score = 0.4
        elif source_type == "ATTACK_HARNESS":
            provenance_score = 0.8
        else:
            provenance_score = 0.5
            
        signals["provenance_score"] = provenance_score
        
        # 2. Drift Signal
        if memory.version > 1:
            # Fetch the previous embedding
            stmt = select(MemoryEmbedding).where(MemoryEmbedding.memory_id == memory.id)
            result = await db.execute(stmt)
            old_embedding_record = result.scalars().first()
            
            if old_embedding_record and old_embedding_record.embedding:
                old_vector = old_embedding_record.embedding
                
                # Use numpy for cosine similarity
                similarity = cosine_similarity(old_vector, current_vector)
                distance = 1.0 - similarity
                
                # In Gradual Drift, multiple small drifts or one large drift can happen.
                # A drift distance of > 0.1 might be considered a meaningful semantic shift.
                # We can normalize this distance to a score.
                drift_score = min(1.0, distance * 2.0)
                signals["drift_magnitude"] = float(distance)
            else:
                signals["drift_magnitude"] = 0.0
        else:
            signals["drift_magnitude"] = 0.0
            
        signals["drift_score"] = drift_score
        
        # Weighted Final Score
        # Give higher weight to drift if it's an update, otherwise provenance heavily influences.
        if memory.version > 1:
            final_score = (drift_score * 0.7) + (provenance_score * 0.3)
        else:
            final_score = provenance_score
            
        is_suspicious = final_score > self.THRESHOLD
        
        # Store result
        anomaly_result = await anomaly_result_repo.create(db, {
            "memory_id": memory.id,
            "memory_version": memory.version,
            "score": final_score,
            "is_suspicious": is_suspicious,
            "signals": signals
        })
        
        return anomaly_result

anomaly_service = AnomalyDetectionService()
