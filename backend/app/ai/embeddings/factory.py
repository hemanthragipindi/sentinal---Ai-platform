from app.core.config import settings
from app.ai.embeddings.base import BaseEmbeddings
from app.ai.embeddings.huggingface import HuggingFaceEmbeddings
import logging

logger = logging.getLogger(__name__)

class EmbeddingsFactory:
    _instance: BaseEmbeddings | None = None

    @classmethod
    def get_embeddings(cls) -> BaseEmbeddings:
        if cls._instance is None:
            provider = settings.EMBEDDING_PROVIDER.lower()
            if provider == "huggingface":
                cls._instance = HuggingFaceEmbeddings()
                logger.info(f"Initialized HuggingFace Embeddings using model: {cls._instance.model}")
            else:
                # Default fallback
                logger.warning(f"Unknown embedding provider '{provider}', defaulting to HuggingFace")
                cls._instance = HuggingFaceEmbeddings()
        return cls._instance
