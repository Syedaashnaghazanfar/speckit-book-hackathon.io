---
title: Physical AI Backend
emoji: >
colorFrom: blue
colorTo: purple
sdk: docker
pinned: false
app_port: 7860
---

# Physical AI & Humanoid Robotics Textbook - Backend API

Backend API for the AI-native interactive textbook with RAG chatbot powered by Gemini and Qdrant.

## Features

- > **RAG Chatbot**: Semantic search over course content using Qdrant vector database
- >à **Gemini AI**: Powered by Google's Gemini model for intelligent responses
- =Ú **Course Content**: Covers ROS 2, Gazebo, Isaac Sim, and VLA for humanoid robotics
- = **CORS Enabled**: Configured for Vercel frontend integration
- ¡ **FastAPI**: High-performance async API

## Environment Variables

Configure these in your Hugging Face Space settings:

```
QDRANT_API_KEY=your-qdrant-api-key
QDRANT_URL=your-qdrant-url
GEMINI_API_KEY=your-gemini-api-key
CORS_ORIGINS=http://localhost:3000,https://speckit-book-hackathon-io.vercel.app
ENVIRONMENT=production
RATE_LIMIT_PER_MINUTE=100
```

## API Endpoints

- `GET /` - API information
- `GET /api/health` - Health check
- `POST /api/chat/` - Chat with RAG chatbot
- `POST /api/translate/` - Translation endpoint

## Docker Deployment

This Space uses Docker with port 7860 (Hugging Face default).

## Frontend

Frontend deployed at: https://speckit-book-hackathon-io.vercel.app/

## Tech Stack

- FastAPI
- Uvicorn
- Qdrant (Vector Database)
- Google Gemini AI
- FastEmbed (Embeddings)
- Python 3.10
