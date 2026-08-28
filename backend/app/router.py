from fastapi import APIRouter

from app.modules.auth.api import router as auth_router
from app.modules.users.api import router as users_router
from app.modules.chat.api import router as chat_router
from app.modules.memory.api import router as memory_router
from app.modules.retrieval.api import router as retrieval_router
from app.modules.storage.api import router as storage_router
from app.modules.reports.api import router as reports_router
from app.modules.settings.api import router as settings_router
from app.modules.audit.api import router as audit_router
from app.modules.jobs.api import router as jobs_router
from app.modules.health.api import router as health_router
from app.modules.explainability.api import router as explainability_router

api_router = APIRouter()

# Register all module routers
api_router.include_router(health_router)
api_router.include_router(auth_router)
api_router.include_router(users_router)
api_router.include_router(chat_router)
api_router.include_router(memory_router)
api_router.include_router(retrieval_router)
api_router.include_router(storage_router)
api_router.include_router(reports_router)
api_router.include_router(settings_router)
api_router.include_router(audit_router)
api_router.include_router(jobs_router)
api_router.include_router(explainability_router)
