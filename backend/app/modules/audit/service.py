from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.audit.repository import audit_log_repo
from app.modules.audit.models import AuditLog
from app.core.exceptions import SentinelException

class AuditService:
    async def get_audit_log(self, db: AsyncSession, log_id: str) -> AuditLog:
        log = await audit_log_repo.get_by_id(db, log_id)
        if not log:
            raise SentinelException("Audit log not found", status_code=404)
        return log

audit_service = AuditService()
