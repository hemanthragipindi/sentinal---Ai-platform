from sqlalchemy.ext.asyncio import AsyncSession
import time

from app.modules.retrieval.schemas import RetrievalQuery, RetrievalResponse, RetrievedMemoryResult
from app.modules.retrieval.repository import retrieval_log_repo
from app.ai.embeddings.factory import EmbeddingsFactory
from app.vectorstore.factory import VectorStoreFactory
from app.core.exceptions import SentinelException
import logging

logger = logging.getLogger(__name__)

class RetrievalService:
    async def semantic_search(self, db: AsyncSession, user_id: str, query_in: RetrievalQuery) -> RetrievalResponse:
        start_time = time.time()
        
        # 1. Get embedding for the query string
        try:
            embeddings_client = EmbeddingsFactory.get_embeddings()
            query_vector = await embeddings_client.embed_text(query_in.query)
        except Exception as e:
            logger.error(f"Failed to generate embedding for query: {e}")
            raise SentinelException("Failed to generate embedding for query", status_code=500)
            
        # 2. Perform similarity search in PGVector
        try:
            vector_store = VectorStoreFactory.get_vectorstore(db)
            search_results = await vector_store.similarity_search(
                query_embedding=query_vector,
                k=query_in.top_k,
                filter={"user_id": user_id, "status": "active"}
            )
        except Exception as e:
            logger.error(f"Vector search failed: {e}")
            raise SentinelException("Database vector search failed", status_code=500)
        
        # 3. Log retrieval attempt
        response_time = (time.time() - start_time) * 1000
        log = await retrieval_log_repo.create(db, {
            "conversation_id": query_in.conversation_id,
            "query": query_in.query,
            "top_k": query_in.top_k,
            "response_time": response_time
        })
        await db.commit()
        
        # Format results
        results = []
        for idx, res in enumerate(search_results):
            results.append(RetrievedMemoryResult(
                memory_id=res["id"],
                similarity_score=res["similarity_score"],
                rank=idx + 1,
                memory={
                    "id": res["id"],
                    "title": res["title"],
                    "content": res["content"]
                }
            ))
            
        return RetrievalResponse(
            query=query_in.query,
            top_k=query_in.top_k,
            response_time=response_time,
            results=results
        )

retrieval_service = RetrievalService()
