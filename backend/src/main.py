"""
FastAPI application entry point for Physical AI & Humanoid Robotics Textbook.

This module initializes the FastAPI application with:
- CORS middleware for frontend communication
- Rate limiting middleware
- Error handling middleware
- Health check endpoint
- API routes for RAG chatbot
"""

from fastapi import FastAPI
import uvicorn

from .middleware.cors import setup_cors
# from .middleware.rate_limit import setup_rate_limiting  # Temporarily disabled
from .middleware.error_handler import setup_error_handlers
from .api.health import router as health_router
from .api.chat import router as chat_router
from .api.translate import router as translate_router
from .api.auth import router as auth_router
from .services.db import db

# Application metadata
app = FastAPI(
    title="Physical AI & Humanoid Robotics Textbook API",
    description="Backend API for AI-native interactive textbook with RAG chatbot",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Setup middleware
setup_cors(app)
# setup_rate_limiting(app)  # Temporarily disabled - will fix later
setup_error_handlers(app)

@app.on_event("startup")
async def startup_event():
    await db.connect()

@app.on_event("shutdown")
async def shutdown_event():
    await db.disconnect()

# Include routers
app.include_router(health_router)
app.include_router(auth_router)
app.include_router(chat_router)
app.include_router(translate_router)

@app.get("/")
async def root():
    """Root endpoint - API information."""
    return {
        "message": "Physical AI & Humanoid Robotics Textbook API",
        "version": "1.0.0",
        "docs": "/docs",
        "health": "/api/health"
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
