from abc import ABC, abstractmethod
from typing import List, Dict, Any

class BaseVectorStore(ABC):
    """Base class for vector databases."""
    
    @abstractmethod
    async def add_texts(self, texts: List[str], metadatas: List[Dict[str, Any]], embeddings: List[List[float]]) -> List[str]:
        """Add texts and their embeddings to the store."""
        pass
        
    @abstractmethod
    async def similarity_search(self, query_embedding: List[float], k: int = 5, filter: Dict[str, Any] = None) -> List[Dict[str, Any]]:
        """Search for similar texts by embedding."""
        pass
        
    @abstractmethod
    async def delete(self, ids: List[str]) -> bool:
        """Delete vectors by their IDs."""
        pass
