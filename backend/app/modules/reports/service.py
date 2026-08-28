from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timezone

from app.modules.reports.repository import report_repo
from app.modules.reports.schemas import ReportCreate
from app.modules.reports.models import Report
from app.core.exceptions import SentinelException
from app.database.models.enums import ReportStatus

class ReportService:
    async def create_report(self, db: AsyncSession, user_id: str, report_in: ReportCreate) -> Report:
        data = report_in.model_dump()
        data["user_id"] = user_id
        data["status"] = ReportStatus.PENDING
        data["generated_by"] = user_id
        
        rep = await report_repo.create(db, data)
        await db.commit()
        return rep

    async def get_report(self, db: AsyncSession, user_id: str, report_id: str) -> Report:
        rep = await report_repo.get_by_id(db, report_id)
        if not rep or str(rep.user_id) != str(user_id):
            raise SentinelException("Report not found", status_code=404)
        return rep

report_service = ReportService()
