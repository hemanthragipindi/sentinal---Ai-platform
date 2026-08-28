from pydantic import BaseModel, Field
from typing import Optional, List, Dict, Any
from datetime import datetime

class AttackResult(BaseModel):
    attack_type: str
    target_user_id: str
    success: bool
    agent_response: Optional[str] = None
    test_query: Optional[str] = None
    details: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)

class DirectInjectionParams(BaseModel):
    title: str = "Injected Memory"
    content: str
    importance_score: float = 1.0

class IndirectInjectionParams(BaseModel):
    title: str = "Benign Document"
    benign_content: str
    malicious_instruction: str

class GradualDriftParams(BaseModel):
    title: str = "Trusted Configuration"
    initial_content: str
    drift_steps: List[str]

class ImpersonationParams(BaseModel):
    title: str = "Authoritative Source"
    source_identity: str
    malicious_content: str
