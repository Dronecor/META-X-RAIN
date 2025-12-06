from typing import List, Dict, Any
from langchain_core.embeddings import Embeddings
from langchain_community.vectorstores import Pinecone
from backend.config import settings
import time

class MockEmbeddings(Embeddings):
    """
    Mock embeddings for development without burning API credits or large local model downloads.
    Returns random vectors of correct dimension.
    """
    def __init__(self, dimension: int = 1536):
        self.dimension = dimension

    def embed_documents(self, texts: List[str]) -> List[List[float]]:
        # import numpy as np
        # return np.random.rand(len(texts), self.dimension).tolist()
        return [[0.1] * self.dimension for _ in texts] # constant for determinism in mock

    def embed_query(self, text: str) -> List[float]:
        return [0.1] * self.dimension

class RAGService:
    def __init__(self):
        # In production, use OpenAIEmbeddings or HuggingFaceEmbeddings
        # self.embeddings = OpenAIEmbeddings(api_key=...)
        self.embeddings = MockEmbeddings(dimension=1536)
        
        self.vector_store = None
        # Lazy load or connect to Pinecone/FAISS here
        # if settings.PINECONE_API_KEY:
        #     self.vector_store = Pinecone.from_existing_index(...)

    def search_similar_products(self, query: str, k: int = 3) -> List[Dict[str, Any]]:
        """
        Search for similar products based on text query.
        """
        # Mock response for now
        print(f"[MOCK] RAG Search for: {query}")
        return [
            {"id": 1, "name": "Classic White T-Shirt", "price": 29.99, "similarity": 0.95},
            {"id": 2, "name": "Blue Denim Jeans", "price": 59.99, "similarity": 0.88},
            {"id": 3, "name": "Leather Jacket", "price": 120.00, "similarity": 0.82}
        ]

    def add_product_to_index(self, product_text: str, metadata: Dict[str, Any]):
        """
        Embed and index a product.
        """
        # self.vector_store.add_texts([product_text], metadatas=[metadata])
        print(f"[MOCK] Indexed product: {metadata.get('name')}")

rag_service = RAGService()
