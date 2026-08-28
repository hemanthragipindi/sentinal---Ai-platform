from app.core.config import settings
from app.ai.llm.base import BaseLLM
from app.ai.llm.huggingface import HuggingFaceLLM
import logging

logger = logging.getLogger(__name__)

class LLMFactory:
    _instance: BaseLLM | None = None

    @classmethod
    def get_llm(cls) -> BaseLLM:
        if cls._instance is None:
            provider = settings.LLM_PROVIDER.lower()
            if provider == "huggingface":
                cls._instance = HuggingFaceLLM()
                logger.info(f"Initialized HuggingFace LLM using model: {cls._instance.model}")
            else:
                logger.warning(f"Unknown LLM provider '{provider}', defaulting to HuggingFace")
                cls._instance = HuggingFaceLLM()
        return cls._instance
