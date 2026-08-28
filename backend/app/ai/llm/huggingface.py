from typing import AsyncGenerator
from app.core.config import settings
from app.ai.llm.base import BaseLLM
from app.core.exceptions import SentinelException
from huggingface_hub import AsyncInferenceClient

class HuggingFaceLLM(BaseLLM):
    def __init__(self):
        self.model = settings.LLM_MODEL_NAME or "HuggingFaceH4/zephyr-7b-beta"
        self.api_key = settings.HF_TOKEN
        
        if not self.api_key:
            raise SentinelException(
                message="HuggingFace API key not configured for LLM.",
                status_code=500
            )
            
        # Let the official SDK handle all routing and endpoints
        self.client = AsyncInferenceClient(token=self.api_key)

    async def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        try:
            response = await self.client.chat_completion(
                model=self.model,
                messages=messages,
                max_tokens=512,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise SentinelException(
                message=f"HuggingFace LLM Error: {str(e)}",
                status_code=500
            )

    async def stream_response(self, prompt: str, system_prompt: str | None = None) -> AsyncGenerator[str, None]:
        # Simple non-streaming fallback
        response = await self.generate_response(prompt, system_prompt)
        yield response
        
    async def chat(self, messages: list[dict]) -> str:
        try:
            response = await self.client.chat_completion(
                model=self.model,
                messages=messages,
                max_tokens=512,
                temperature=0.7
            )
            return response.choices[0].message.content.strip()
        except Exception as e:
            raise SentinelException(
                message=f"HuggingFace LLM Error: {str(e)}",
                status_code=500
            )
