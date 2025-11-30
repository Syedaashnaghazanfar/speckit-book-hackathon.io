"""
Chat API endpoint for RAG-powered textbook assistant.

Handles:
- User queries
- Context retrieval
- Response generation
- Citation formatting
- Error handling
"""

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, Field
from typing import List, Dict, Optional
import logging

from ..services.qdrant_client import qdrant_service
from ..services.embeddings import embedding_service
from ..services.query_processor import query_processor
from ..services.generation import generation_service

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/api/chat", tags=["chat"])


# Request/Response Models
class ChatRequest(BaseModel):
    """Chat request model."""
    query: str = Field(..., min_length=3, max_length=500, description="User question")
    top_k: Optional[int] = Field(5, ge=1, le=10, description="Number of sources to retrieve")


class Source(BaseModel):
    """Source citation model."""
    excerpt_num: int
    week: int
    section: str
    score: float


class ChatResponse(BaseModel):
    """Chat response model."""
    answer: str
    sources: List[Source]
    has_answer: bool
    confidence: str  # 'high', 'medium', 'low'
    num_sources: int
    query_processed: str  # Show enhanced query for debugging


@router.post("/", response_model=ChatResponse, status_code=status.HTTP_200_OK)
async def chat(request: ChatRequest):
    """
    Process chat query and return RAG-grounded response.

    Args:
        request: ChatRequest with user query and optional filters

    Returns:
        ChatResponse with answer, sources, and metadata

    Raises:
        HTTPException: If query processing fails
    """
    try:
        logger.info(f"Received chat request: '{request.query}'")

        # Step 1: Process query (expand acronyms, classify intent)
        query_info = query_processor.process_query(request.query)
        enhanced_query = query_info['enhanced_query']

        # Step 2: Generate query embedding
        logger.info(f"Generating embedding for query: '{enhanced_query}'")
        query_embedding = await embedding_service.generate_embedding(enhanced_query)

        # Step 3: Retrieve relevant chunks from Qdrant
        logger.info(f"Searching Qdrant for top {request.top_k} similar chunks")
        retrieved_chunks = await qdrant_service.search_similar(
            query_vector=query_embedding,
            limit=request.top_k,
            score_threshold=0.65  # Lowered from 0.7 for better recall
        )

        if not retrieved_chunks:
            logger.warning("No relevant chunks found")
            return ChatResponse(
                answer="I couldn't find relevant information in the textbook to answer your question. Please try rephrasing or asking about a different topic covered in the course.",
                sources=[],
                has_answer=False,
                confidence='low',
                num_sources=0,
                query_processed=enhanced_query
            )

        logger.info(f"Retrieved {len(retrieved_chunks)} chunks")

        # Step 4: Generate response using Gemini
        result = await generation_service.generate_response(
            query=request.query,
            retrieved_chunks=retrieved_chunks
        )

        # Step 5: Format response
        return ChatResponse(
            answer=result['answer'],
            sources=[Source(**s) for s in result['sources']],
            has_answer=result['has_answer'],
            confidence=result['confidence'],
            num_sources=result['num_sources'],
            query_processed=enhanced_query
        )

    except Exception as e:
        logger.error(f"Chat request failed: {str(e)}", exc_info=True)
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process chat request: {str(e)}"
        )


@router.get("/health", status_code=status.HTTP_200_OK)
async def health_check():
    """Health check for chat service."""
    return {
        "status": "healthy",
        "service": "chat",
        "retrieval": "qdrant",
        "generation": "gemini"
    }
