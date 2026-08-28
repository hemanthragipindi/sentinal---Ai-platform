from app.core.config import settings
from app.vectorstore.base import BaseVectorStore
from app.vectorstore.pgvector import PGVectorStore
from sqlalchemy.ext.asyncio import AsyncSession
import logging

logger = logging.getLogger(__name__)

class VectorStoreFactory:
    @classmethod
    def get_vectorstore(cls, db: AsyncSession) -> BaseVectorStore:
        provider = settings.VECTORSTORE_PROVIDER.lower()
        if provider == "pgvector":
            return PGVectorStore(db)
        else:
            logger.warning(f"Unknown vectorstore provider '{provider}', defaulting to pgvector")
            return PGVectorStore(db)
