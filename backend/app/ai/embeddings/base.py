from abc import ABC, abstractmethod
from typing import List

class BaseEmbeddings(ABC):
    """Base class for all embedding providers."""
    
    @abstractmethod
    async def embed_text(self, text: str) -> List[float]:
        """Embed a single piece of text."""
        pass
        
    @abstractmethod
    async def embed_batch(self, texts: List[str]) -> List[List[float]]:
        """Embed a batch of texts."""
        pass
        
    @abstractmethod
    def get_dimension(self) -> int:
        """Return the dimension of the embeddings."""
        pass
