"""
Qdrant vector database client service.

Handles connection and operations with Qdrant Cloud for vector embeddings.
"""

from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
from typing import List, Dict, Optional
from uuid import UUID
import logging

from ..config import settings

logger = logging.getLogger(__name__)


class QdrantService:
    """Service for interacting with Qdrant vector database."""

    def __init__(self):
        """Initialize Qdrant client connection."""
        self.client = QdrantClient(
            url=settings.qdrant_url,
            api_key=settings.qdrant_api_key,
            timeout=60.0  # Increased timeout to prevent ReadTimeout
        )
        self.collection_name = "textbook_embeddings"

    async def create_collection(self, vector_size: int = 384) -> None:
        """
        Create the embeddings collection if it doesn't exist.

        Creates a collection with:
        - 384 dimensions (FastEmbed BAAI/bge-small-en-v1.5)
        - Cosine distance metric

        Args:
            vector_size: Embedding dimension size (default: 384 for bge-small-en-v1.5)
        """
        try:
            collections = self.client.get_collections().collections
            collection_exists = any(
                col.name == self.collection_name for col in collections
            )

            if not collection_exists:
                self.client.create_collection(
                    collection_name=self.collection_name,
                    vectors_config=VectorParams(
                        size=vector_size,
                        distance=Distance.COSINE
                    )
                )
                logger.info(f"Created collection: {self.collection_name} with {vector_size} dimensions")
            else:
                logger.info(f"Collection already exists: {self.collection_name}")

        except Exception as e:
            logger.error(f"Failed to create collection: {str(e)}")
            raise

    async def upsert_embeddings(
        self,
        embeddings: List[Dict],
        batch_size: int = 50
    ) -> None:
        """
        Insert or update embeddings in Qdrant in batches.

        Args:
            embeddings: List of embedding dictionaries with:
                - id: Unique identifier
                - vector: Embedding vector (3072 dimensions)
                - payload: Metadata (module, week, section, content, etc.)
            batch_size: Number of embeddings to upload per batch (default: 50)
        """
        try:
            points = [
                PointStruct(
                    id=str(emb["id"]),
                    vector=emb["vector"],
                    payload=emb["payload"]
                )
                for emb in embeddings
            ]

            # Upload in batches to avoid timeouts
            total_uploaded = 0
            for i in range(0, len(points), batch_size):
                batch = points[i:i + batch_size]
                self.client.upsert(
                    collection_name=self.collection_name,
                    points=batch,
                    wait=True  # Wait for operation to complete
                )
                total_uploaded += len(batch)
                logger.info(f"Batch {i//batch_size + 1}: Uploaded {total_uploaded}/{len(points)} embeddings")

            logger.info(f"✅ Successfully upserted all {len(points)} embeddings")

        except Exception as e:
            logger.error(f"Failed to upsert embeddings: {str(e)}")
            raise

    async def search_similar(
        self,
        query_vector: List[float],
        limit: int = 5,
        score_threshold: float = 0.7
    ) -> List[Dict]:
        """
        Search for similar embeddings.

        Args:
            query_vector: Query embedding vector (3072 dimensions)
            limit: Maximum number of results to return
            score_threshold: Minimum similarity score (0.0-1.0)

        Returns:
            List of search results with scores and metadata
        """
        try:
            # Use query_points for newer Qdrant client API
            from qdrant_client.models import models

            results = self.client.query_points(
                collection_name=self.collection_name,
                query=query_vector,
                limit=limit,
                score_threshold=score_threshold
            )

            # Handle both QueryResponse and list of ScoredPoint
            if hasattr(results, 'points'):
                points = results.points
            else:
                points = results

            return [
                {
                    "id": result.id,
                    "score": result.score,
                    "payload": result.payload
                }
                for result in points
            ]

        except Exception as e:
            logger.error(f"Search failed: {str(e)}")
            raise


# Global instance
qdrant_service = QdrantService()
