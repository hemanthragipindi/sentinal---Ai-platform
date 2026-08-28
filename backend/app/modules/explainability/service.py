from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import logging
from typing import Optional

from app.modules.explainability.schemas import ExplanationResult
from app.modules.memory.repository import memory_repo
from app.modules.threat_detection.models import AnomalyResult, QuarantinedMemory
from app.database.models.enums import MemoryStatus
from app.core.exceptions import SentinelException
from app.modules.threat_detection.anomaly_service import anomaly_service

logger = logging.getLogger(__name__)

class ExplanationService:
    async def get_explanation(self, db: AsyncSession, memory_id: str) -> ExplanationResult:
        # Fetch Memory and Provenance
        memory = await memory_repo.get_by_id_with_provenance(db, memory_id)
        if not memory:
            raise SentinelException("Memory not found", status_code=404)

        # Fetch latest AnomalyResult
        stmt_a = select(AnomalyResult).where(AnomalyResult.memory_id == memory_id).order_by(AnomalyResult.id.desc())
        result_a = await db.execute(stmt_a)
        anomaly = result_a.scalars().first()

        # Fetch QuarantinedMemory
        stmt_q = select(QuarantinedMemory).where(QuarantinedMemory.memory_id == memory_id)
        result_q = await db.execute(stmt_q)
        quarantine_record = result_q.scalars().first()

        # Build Data Fields
        decision = "UNKNOWN"
        threshold = anomaly_service.THRESHOLD
        anomaly_score = anomaly.score if anomaly else None
        
        contributing_signals = []
        provenance_evidence = None
        drift_evidence = None
        quarantine_action = None
        rollback_action = None
        counterfactual = None

        if quarantine_record:
            if quarantine_record.status == "active":
                decision = "QUARANTINED"
                quarantine_action = quarantine_record.reason
                counterfactual = "If the memory was demonstrably retrievable, without quarantine, it would have remained available to normal retrieval and could have continued influencing the agent."
            elif quarantine_record.status == "rolled_back":
                decision = "ROLLED BACK"
                quarantine_action = quarantine_record.reason
                rollback_action = "Restored to a previous trusted version."
                counterfactual = "Without rollback, the poisoned version would have remained active and could have influenced the agent."
            else:
                decision = memory.status.name if hasattr(memory.status, 'name') else memory.status
        else:
            decision = "ACTIVE"
            counterfactual = "No security action was needed, so the memory proceeded to normal processing."

        idx = 1
        summary_lines = []
        if decision == "QUARANTINED":
            summary_lines.append("Memory was quarantined because:\n")
        elif decision == "ROLLED BACK":
            summary_lines.append("Memory was previously quarantined and has been rolled back because:\n")
        elif decision == "ACTIVE" and anomaly and anomaly.is_suspicious:
            summary_lines.append("Memory was flagged as suspicious but remained active because:\n")
        else:
            summary_lines.append("Memory is considered safe because:\n")

        if anomaly and anomaly.signals:
            if "drift_magnitude" in anomaly.signals and anomaly.signals["drift_magnitude"] > 0.0:
                drift_mag = anomaly.signals["drift_magnitude"]
                drift_evidence = f"Magnitude: {drift_mag:.2f}"
                msg = f"{idx}. Semantic drift from previous version (magnitude: {drift_mag:.2f})."
                contributing_signals.append(msg)
                summary_lines.append(msg)
                idx += 1
                
        if memory.provenance:
            src = memory.provenance.source_type
            provenance_evidence = f"Source Type: {src}"
            msg = f"{idx}. The memory originated from {src}."
            contributing_signals.append(msg)
            summary_lines.append(msg)
            idx += 1
            
        if anomaly_score is not None:
            msg = f"{idx}. The anomaly score was {anomaly_score:.2f}."
            contributing_signals.append(msg)
            summary_lines.append(msg)
            idx += 1
            
            msg = f"{idx}. The configured threshold was {threshold:.2f}."
            contributing_signals.append(msg)
            summary_lines.append(msg)
            idx += 1
            
        summary_lines.append(f"\nDecision:\n{decision}")
        
        summary = "\n".join(summary_lines)

        return ExplanationResult(
            memory_id=memory_id,
            decision=decision,
            anomaly_score=anomaly_score,
            threshold=threshold,
            summary=summary,
            contributing_signals=contributing_signals,
            provenance_evidence=provenance_evidence,
            drift_evidence=drift_evidence,
            quarantine_action=quarantine_action,
            rollback_action=rollback_action,
            counterfactual=counterfactual
        )

explanation_service = ExplanationService()
