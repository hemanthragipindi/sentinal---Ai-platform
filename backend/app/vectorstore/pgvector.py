from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from typing import List, Dict, Any
from app.vectorstore.base import BaseVectorStore

class PGVectorStore(BaseVectorStore):
    def __init__(self, db: AsyncSession):
        self.db = db

    async def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], embeddings: List[List[float]]) -> List[str]:
        raise NotImplementedError("Use MemoryRepository to insert memories with embeddings.")

    async def similarity_search(self, query_embedding: List[float], k: int = 5, filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        # Using pgvector cosine distance operator <=>
        
        embedding_str = "[" + ",".join(map(str, query_embedding)) + "]"
        
        query = f"""
            SELECT m.id, m.title, m.content, m.memory_type, me.embedding <=> '{embedding_str}' AS distance
            FROM memories m
            JOIN memory_embeddings me ON m.id = me.memory_id
            WHERE 1=1
        """
        
        params = {}
        if filter:
            if "user_id" in filter:
                query += " AND m.user_id = :user_id"
                params["user_id"] = filter["user_id"]
            if "status" in filter:
                query += " AND m.status = :status"
                params["status"] = filter["status"].value if hasattr(filter["status"], 'value') else filter["status"]
                
        query += " ORDER BY distance ASC LIMIT :limit"
        params["limit"] = k
        
        result = await self.db.execute(text(query), params)
        rows = result.fetchall()
        
        results = []
        for row in rows:
            similarity = 1.0 - float(row.distance)
            results.append({
                "id": str(row.id),
                "title": row.title,
                "content": row.content,
                "memory_type": row.memory_type.value if hasattr(row.memory_type, 'value') else row.memory_type,
                "similarity_score": similarity
            })
            
        return results

    async def delete(self, ids: List[str]) -> bool:
        raise NotImplementedError("Use MemoryRepository to delete memories.")
