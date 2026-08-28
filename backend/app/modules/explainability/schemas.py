from pydantic import BaseModel
from typing import Optional, List

class ExplanationResult(BaseModel):
    memory_id: str
    decision: str
    anomaly_score: Optional[float] = None
    threshold: Optional[float] = None
    summary: str
    contributing_signals: List[str]
    provenance_evidence: Optional[str] = None
    drift_evidence: Optional[str] = None
    quarantine_action: Optional[str] = None
    rollback_action: Optional[str] = None
    counterfactual: Optional[str] = None
