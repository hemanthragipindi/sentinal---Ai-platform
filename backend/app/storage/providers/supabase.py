from typing import Any
from supabase import create_client, Client
from supabase.lib.client_options import ClientOptions
import time

from app.core.config import settings
from app.core.logging import logger

class SupabaseProvider:
    def __init__(self):
        self.url = settings.SUPABASE_URL
        self.key = settings.SUPABASE_KEY
        self._client: Client | None = None
        
        if self.url and self.key:
            self._client = create_client(self.url, self.key)

    def get_client(self) -> Client | None:
        return self._client

    async def check_health(self) -> dict[str, Any]:
        if not self._client:
            return {"status": "Not Configured", "latency_ms": None}
            
        try:
            start_time = time.time()
            # A simple bucket listing to verify the storage API is responsive
            self._client.storage.list_buckets()
            latency_ms = int((time.time() - start_time) * 1000)
            return {"status": "Connected", "latency_ms": latency_ms}
        except Exception as e:
            logger.error(f"Supabase Health Check Failed: {e}")
            return {"status": "Disconnected", "latency_ms": None}

supabase_client = SupabaseProvider()
