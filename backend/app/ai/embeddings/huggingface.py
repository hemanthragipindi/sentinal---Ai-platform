import httpx
from typing import List
from app.core.config import settings
from app.ai.embeddings.base import BaseEmbeddings
from app.core.exceptions import SentinelException

class HuggingFaceEmbeddings(BaseEmbeddings):
    def __init__(self):
        self.model = settings.EMBEDDING_MODEL_NAME or "sentence-transformers/all-MiniLM-L6-v2"
        self.api_key = settings.HF_TOKEN
        base_url = settings.HF_ROUTER_URL or "https://router.huggingface.co/hf-inference"
        self.api_url = f"{base_url}/pipeline/feature-extraction/{self.model}"
        
        if not self.api_key:
            raise SentinelException(
                message="HuggingFace API key not configured.",
                status_code=500
            )

    async def _call_api(self, inputs: list[str]) -> list:
        headers = {"Authorization": f"Bearer {self.api_key}"}
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(
                    self.api_url, 
                    headers=headers, 
                    json={"inputs": inputs, "options": {"wait_for_model": True}}
                )
                response.raise_for_status()
                return response.json()
            except httpx.HTTPStatusError as e:
                raise SentinelException(
                    message=f"HuggingFace API Error: {e.response.text}",
                    status_code=e.response.status_code
                )
            except Exception as e:
                raise SentinelException(
                    message=f"Failed to connect to HuggingFace API: {str(e)}",
                    status_code=500
                )

    async def embed_text(self, text: str) -> List[float]:
        results = await self._call_api([text])
        if not results or not isinstance(results, list):
            raise SentinelException("Invalid response from embedding API", status_code=500)
        # Some HF models return 1D list, some return 2D list
        if isinstance(results[0], list):
            return results[0]
        return results

    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        results = await self._call_api(texts)
        if not results or not isinstance(results, list):
            raise SentinelException("Invalid response from embedding API", status_code=500)
        return results

    def get_dimension(self) -> int:
        # For all-MiniLM-L6-v2 the dim is 384
        if "MiniLM" in self.model:
            return 384
        return 768 # Default fallback
