"""
Health check API endpoint.

Provides service status and health information.
"""

from fastapi import APIRouter
from pydantic import BaseModel
from typing import Dict

router = APIRouter(prefix="/api", tags=["health"])


class HealthResponse(BaseModel):
    """Health check response model."""
    status: str
    services: Dict[str, str]


@router.get("/health", response_model=HealthResponse)
async def health_check():
    """
    Health check endpoint.

    Returns:
        HealthResponse: Service status information
    """
    # TODO: Add actual service health checks for Qdrant and Gemini
    return HealthResponse(
        status="ok",
        services={
            "api": "up",
            "qdrant": "unknown",  # Will be implemented with actual client
            "gemini": "unknown"   # Will be implemented with actual client
        }
    )
