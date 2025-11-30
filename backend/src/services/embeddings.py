"""
FastEmbed embeddings service.

Generates embeddings for text chunks using local FastEmbed models (no API required).
"""

from fastembed import TextEmbedding
from typing import List
import asyncio
import logging

logger = logging.getLogger(__name__)


class EmbeddingService:
    """Service for generating text embeddings using FastEmbed (local model)."""

    def __init__(self, model_name: str = "BAAI/bge-small-en-v1.5"):
        """
        Initialize FastEmbed client with local model.

        Args:
            model_name: FastEmbed model to use. Options:
                - "BAAI/bge-small-en-v1.5" (384 dims, fast, recommended)
                - "sentence-transformers/all-MiniLM-L6-v2" (384 dims)
                - "BAAI/bge-base-en-v1.5" (768 dims, better quality)
        """
        logger.info(f"Initializing FastEmbed with model: {model_name}")
        self.model = TextEmbedding(model_name=model_name)
        self.model_name = model_name

        # Get embedding dimension from first test embedding
        test_embedding = list(self.model.embed(["test"]))[0]
        self.embedding_dim = len(test_embedding)
        logger.info(f"FastEmbed initialized. Embedding dimension: {self.embedding_dim}")

    async def generate_embedding(self, text: str) -> List[float]:
        """
        Generate embedding for a single text.

        Args:
            text: Input text

        Returns:
            Embedding vector (384 dimensions for bge-small-en-v1.5)
        """
        try:
            # Run embedding generation in executor since FastEmbed is CPU-bound
            loop = asyncio.get_event_loop()
            embedding = await loop.run_in_executor(
                None,
                lambda: list(self.model.embed([text]))[0]
            )
            return embedding.tolist() if hasattr(embedding, 'tolist') else list(embedding)

        except Exception as e:
            logger.error(f"Failed to generate embedding: {str(e)}")
            raise

    async def generate_embeddings_batch(
        self,
        texts: List[str],
        batch_size: int = 32
    ) -> List[List[float]]:
        """
        Generate embeddings for multiple texts in batches.

        FastEmbed processes batches locally with no API limits.

        Args:
            texts: List of input texts
            batch_size: Number of texts to process at once (default: 32)

        Returns:
            List of embedding vectors
        """
        all_embeddings = []

        try:
            # Process in batches for memory efficiency
            for i in range(0, len(texts), batch_size):
                batch = texts[i:i + batch_size]

                # Run batch embedding in executor
                loop = asyncio.get_event_loop()
                batch_embeddings = await loop.run_in_executor(
                    None,
                    lambda: list(self.model.embed(batch))
                )

                # Convert numpy arrays to lists
                batch_embeddings = [
                    emb.tolist() if hasattr(emb, 'tolist') else list(emb)
                    for emb in batch_embeddings
                ]

                all_embeddings.extend(batch_embeddings)
                logger.info(f"Generated {len(batch_embeddings)} embeddings (batch {i // batch_size + 1}/{(len(texts) + batch_size - 1) // batch_size})")

            logger.info(f"✅ Total embeddings generated: {len(all_embeddings)}")
            return all_embeddings

        except Exception as e:
            logger.error(f"Failed to generate embeddings: {str(e)}")
            raise


# Global instance (using fast, lightweight model)
embedding_service = EmbeddingService(model_name="BAAI/bge-small-en-v1.5")
