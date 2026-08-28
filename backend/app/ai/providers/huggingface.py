import httpx
from typing import Any
from app.core.config import settings
from app.core.logging import logger
from app.core.exceptions import SentinelException

class HuggingFaceProvider:
    def __init__(self):
        self.base_url = settings.HF_ROUTER_URL
        self.token = settings.HF_TOKEN
        self.headers = {
            "Authorization": f"Bearer {self.token}",
            "Content-Type": "application/json"
        }

    async def check_health(self) -> dict[str, Any]:
        if not self.token or not self.base_url:
            return {"status": "Not Configured", "latency_ms": None}
            
        try:
            async with httpx.AsyncClient() as client:
                # We do a lightweight models call for health ping
                response = await client.get(
                    f"https://huggingface.co/api/models?limit=1", 
                    headers=self.headers,
                    timeout=5.0
                )
                response.raise_for_status()
                return {"status": "Connected", "latency_ms": response.elapsed.microseconds / 1000}
        except Exception as e:
            logger.error(f"HF Health Check Failed: {e}")
            return {"status": "Disconnected", "latency_ms": None}

hf_client = HuggingFaceProvider()
