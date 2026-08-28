from abc import ABC, abstractmethod
from typing import AsyncGenerator

class BaseLLM(ABC):
    """Base class for all LLM providers."""
    
    @abstractmethod
    async def generate_response(self, prompt: str, system_prompt: str | None = None) -> str:
        """Generate a complete text response from the LLM."""
        pass
        
    @abstractmethod
    async def stream_response(self, prompt: str, system_prompt: str | None = None) -> AsyncGenerator[str, None]:
        """Stream the text response from the LLM."""
        pass
        
    @abstractmethod
    async def chat(self, messages: list[dict]) -> str:
        """Generate a response using a conversation history."""
        pass
