import pytest
import sys
import os
from unittest.mock import AsyncMock, patch, MagicMock

backend_path = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../backend'))
if backend_path not in sys.path:
    sys.path.insert(0, backend_path)

from app.modules.explainability.service import ExplanationService
from app.modules.explainability.schemas import ExplanationResult
from app.database.models.enums import MemoryStatus

@pytest.fixture
def mock_db():
    return AsyncMock()

@pytest.mark.asyncio
@patch('app.modules.explainability.service.memory_repo')
async def test_explanation_chain_quarantine(mock_mem_repo, mock_db):
    service = ExplanationService()
    
    # Mock Memory
    mem = MagicMock()
    mem.id = "mem123"
    mem.status = MemoryStatus.QUARANTINED
    mem.provenance = MagicMock()
    mem.provenance.source_type = "ATTACK_HARNESS"
    mock_mem_repo.get_by_id_with_provenance = AsyncMock(return_value=mem)
    
    # Mock Anomaly
    anomaly = MagicMock()
    anomaly.score = 0.91
    anomaly.is_suspicious = True
    anomaly.signals = {"drift_magnitude": 0.82, "provenance_score": 0.8}
    
    # Mock Quarantine Record
    q_record = MagicMock()
    q_record.status = "active"
    q_record.reason = "Suspicious activity detected"
    
    # Set up DB execution returns
    mock_result_a = MagicMock()
    mock_result_a.scalars.return_value.first.return_value = anomaly
    
    mock_result_q = MagicMock()
    mock_result_q.scalars.return_value.first.return_value = q_record
    
    mock_db.execute.side_effect = [mock_result_a, mock_result_q]
    
    # Execute explanation
    result = await service.get_explanation(mock_db, "mem123")
    
    assert result.decision == "QUARANTINED"
    assert result.anomaly_score == 0.91
    assert "ATTACK_HARNESS" in result.provenance_evidence
    assert "0.82" in result.drift_evidence
    assert "without quarantine, it would have remained available" in result.counterfactual
    
@pytest.mark.asyncio
@patch('app.modules.explainability.service.memory_repo')
async def test_explanation_chain_rollback(mock_mem_repo, mock_db):
    service = ExplanationService()
    
    mem = MagicMock()
    mem.id = "mem123"
    mem.status = MemoryStatus.ACTIVE
    mem.provenance = MagicMock()
    mem.provenance.source_type = "ATTACK_HARNESS"
    mock_mem_repo.get_by_id_with_provenance = AsyncMock(return_value=mem)
    
    anomaly = MagicMock()
    anomaly.score = 0.95
    anomaly.is_suspicious = True
    anomaly.signals = {"drift_magnitude": 0.9, "provenance_score": 0.8}
    
    q_record = MagicMock()
    q_record.status = "rolled_back"
    q_record.reason = "Suspicious activity detected"
    
    mock_result_a = MagicMock()
    mock_result_a.scalars.return_value.first.return_value = anomaly
    
    mock_result_q = MagicMock()
    mock_result_q.scalars.return_value.first.return_value = q_record
    
    mock_db.execute.side_effect = [mock_result_a, mock_result_q]
    
    result = await service.get_explanation(mock_db, "mem123")
    
    assert result.decision == "ROLLED BACK"
    assert result.rollback_action is not None
    assert "Without rollback, the poisoned version would have remained active" in result.counterfactual
