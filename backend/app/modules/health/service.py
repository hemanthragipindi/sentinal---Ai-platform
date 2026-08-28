import time
from datetime import datetime, timezone
from sqlalchemy import text
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.config import settings
from app.core.logging import logger
from app.modules.health.schemas import HealthResponse
from app.vectorstore.providers.pgvector import pgvector_client
from app.storage.providers.supabase import supabase_client
from app.ai.providers.huggingface import hf_client

class HealthService:
    async def check_health(self, db: AsyncSession) -> dict:
        health_data = {
            "version": settings.VERSION,
            "timestamp": datetime.now(timezone.utc).isoformat(),
            "status": "Healthy",
            "database": {"status": "Disconnected", "latency_ms": None},
            "pgvector": {"status": "Disconnected", "latency_ms": None},
            "supabase": {"status": "Disconnected", "latency_ms": None},
            "huggingface": {"status": "Disconnected", "latency_ms": None},
        }

        # Check PostgreSQL
        try:
            start_time = time.time()
            await db.execute(text("SELECT 1"))
            health_data["database"]["latency_ms"] = int((time.time() - start_time) * 1000)
            health_data["database"]["status"] = "Connected"
        except Exception as e:
            logger.error(f"Database Health Check Failed: {e}")
            health_data["status"] = "Degraded"

        # Check pgvector
        pg_res = await pgvector_client.check_health(db)
        health_data["pgvector"] = pg_res
        if pg_res["status"] != "Connected":
            health_data["status"] = "Degraded"

        # Check Supabase
        sb_res = await supabase_client.check_health()
        health_data["supabase"] = sb_res
        if sb_res["status"] != "Connected":
            health_data["status"] = "Degraded"

        # Check Hugging Face
        hf_res = await hf_client.check_health()
        health_data["huggingface"] = hf_res
        if hf_res["status"] != "Connected":
            health_data["status"] = "Degraded"

        return health_data

health_service = HealthService()
