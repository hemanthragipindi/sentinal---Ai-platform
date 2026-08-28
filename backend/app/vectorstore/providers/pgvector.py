from typing import Any
from sqlalchemy import select, text
from sqlalchemy.ext.asyncio import AsyncSession
import time
from app.core.logging import logger

class PgVectorProvider:
    @staticmethod
    async def check_health(db: AsyncSession) -> dict[str, Any]:
        try:
            start_time = time.time()
            result = await db.execute(text("SELECT extname FROM pg_extension WHERE extname = 'vector'"))
            has_vector = result.scalar_one_or_none() is not None
            
            latency_ms = int((time.time() - start_time) * 1000)
            
            if has_vector:
                return {"status": "Connected", "latency_ms": latency_ms}
            return {"status": "Not Installed", "latency_ms": latency_ms}
        except Exception as e:
            logger.error(f"PgVector Health Check Failed: {e}")
            return {"status": "Disconnected", "latency_ms": None}

pgvector_client = PgVectorProvider()
