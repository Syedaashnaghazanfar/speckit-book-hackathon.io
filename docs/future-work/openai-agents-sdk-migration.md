# OpenAI Agents SDK Migration - Future Work

**Status:** Planned for future implementation
**Priority:** Medium
**Estimated Effort:** 2-3 days
**Created:** 2025-12-01

## Overview

Migrate the current custom RAG chatbot implementation to use the **OpenAI Agents Python SDK** with **Gemini models** (via LiteLLM integration). This will provide better conversation management, tool calling, and multi-agent capabilities.

## Current Implementation

The chatbot currently uses:
- **Backend:** FastAPI custom implementation
- **AI Model:** Google Gemini AI (direct API calls)
- **Vector DB:** Qdrant for RAG embeddings
- **Embeddings:** FastEmbed (BAAI/bge-small-en-v1.5)
- **Conversation:** Custom state management

**Files:**
- `backend/src/api/chat.py` - Chat endpoint
- `backend/src/services/generation.py` - Gemini response generation
- `backend/src/services/query_processor.py` - Query processing
- `backend/src/services/qdrant_client.py` - Vector search
- `backend/src/services/embeddings.py` - Embedding generation

## Proposed Architecture

### Technology Stack

```python
# Dependencies to add
openai-agents-python>=0.2.9
litellm>=1.30.0
```

### Key Components

1. **OpenAI Agents SDK**
   - Agent orchestration and conversation management
   - Built-in tracing and debugging
   - Multi-agent handoff support
   - Session and state management

2. **LiteLLM Integration**
   - Connect Gemini models to OpenAI Agents SDK
   - Model: `gemini/gemini-2.0-flash` or `gemini/gemini-1.5-pro`
   - Unified interface for multiple LLM providers

3. **Function Tools**
   - Convert Qdrant search to agent function tools
   - RAG retrieval as callable functions
   - Context injection tools

## Implementation Plan

### Phase 1: Setup (Est. 4 hours)

**Task 1.1:** Install Dependencies
```bash
cd backend
pip install openai-agents-python litellm
pip freeze > requirements.txt
```

**Task 1.2:** Create Agent Service Module
- Create `backend/src/services/agent_service.py`
- Initialize LiteLLM with Gemini credentials
- Set up basic agent configuration

### Phase 2: Function Tools (Est. 6 hours)

**Task 2.1:** Create RAG Function Tools

```python
from agents import function_tool

@function_tool
def search_course_content(query: str, top_k: int = 5) -> dict:
    """
    Search the Physical AI & Robotics course content using RAG.

    Args:
        query: User's question or search query
        top_k: Number of relevant excerpts to retrieve

    Returns:
        Dictionary with sources and content excerpts
    """
    # Use existing Qdrant service
    from .qdrant_client import qdrant_service
    from .embeddings import embedding_service

    # Generate query embedding
    query_embedding = embedding_service.generate_embedding(query)

    # Search Qdrant
    results = qdrant_service.search_similar(
        query_vector=query_embedding,
        limit=top_k,
        score_threshold=0.7
    )

    return {
        "sources": results,
        "num_sources": len(results),
        "query_processed": query
    }
```

**Task 2.2:** Create Additional Tools (Optional)
- Translation tool (if needed)
- Course navigation tool
- Feedback collection tool

### Phase 3: Agent Configuration (Est. 4 hours)

**Task 3.1:** Configure Gemini Agent

```python
from agents import Agent, Runner
from agents.extensions.models.litellm_model import LitellmModel
from .config import settings

# Initialize Gemini via LiteLLM
textbook_agent = Agent(
    name="Physical AI Textbook Assistant",
    instructions="""
    You are an AI assistant for the Physical AI & Humanoid Robotics textbook.

    Your role:
    - Answer questions about ROS 2, Gazebo, Isaac Sim, and VLA
    - Provide accurate technical information from the course content
    - Cite sources when answering questions
    - Be helpful, clear, and educational

    When a user asks a question:
    1. Use the search_course_content tool to find relevant information
    2. Synthesize the information into a clear, comprehensive answer
    3. Include source citations (Week number, section)
    4. If the answer isn't in the course content, say so clearly
    """,
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key=settings.gemini_api_key
    ),
    tools=[search_course_content],
)
```

**Task 3.2:** Add Conversation Config

```python
from agents import RunConfig

run_config = RunConfig(
    max_turns=10,  # Limit conversation turns
    temperature=0.7,
    max_tokens=2000,
)
```

### Phase 4: API Integration (Est. 4 hours)

**Task 4.1:** Update FastAPI Endpoint

```python
# backend/src/api/chat.py

from agents import Runner
from ..services.agent_service import textbook_agent, run_config

@router.post("/chat/")
async def chat(request: ChatRequest):
    """
    Chat endpoint using OpenAI Agents SDK with Gemini.
    """
    try:
        # Run agent with user query
        result = await Runner.run(
            textbook_agent,
            request.query,
            config=run_config
        )

        # Extract sources from tool calls
        sources = []
        if result.tool_calls:
            for tool_call in result.tool_calls:
                if tool_call.tool_name == "search_course_content":
                    sources = tool_call.result.get("sources", [])

        return ChatResponse(
            answer=result.final_output,
            sources=sources,
            has_answer=len(sources) > 0,
            confidence="high" if len(sources) >= 3 else "medium",
            num_sources=len(sources),
            query_processed=request.query
        )

    except Exception as e:
        logger.error(f"Agent error: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
```

**Task 4.2:** Add Session Management (Optional)
- Implement conversation history
- Add session IDs for multi-turn conversations
- Store context between requests

### Phase 5: Testing (Est. 6 hours)

**Task 5.1:** Unit Tests
- Test function tools independently
- Test agent initialization
- Test LiteLLM connection

**Task 5.2:** Integration Tests
- Test full chat flow
- Test with various queries
- Test error handling

**Task 5.3:** Performance Testing
- Compare response times vs current implementation
- Test with concurrent requests
- Monitor token usage

### Phase 6: Deployment (Est. 4 hours)

**Task 6.1:** Update Dependencies
```bash
# Update requirements.txt
pip freeze > requirements.txt

# Update Dockerfile if needed
# Ensure LiteLLM and OpenAI Agents SDK are installed
```

**Task 6.2:** Environment Configuration
```bash
# Add to .env or Hugging Face Secrets
GEMINI_API_KEY=your_gemini_key
LITELLM_LOG_LEVEL=INFO
```

**Task 6.3:** Deploy to Hugging Face
- Push updated code
- Set environment variables
- Test deployed version

## Benefits of Migration

### 1. Better Architecture
- ✅ Separation of concerns (agents vs tools vs models)
- ✅ Standardized conversation management
- ✅ Built-in tracing and debugging

### 2. Enhanced Features
- ✅ Multi-agent handoffs (future: translate agent, tutor agent)
- ✅ Guardrails for safety and quality
- ✅ Session management for multi-turn conversations
- ✅ Built-in function calling

### 3. Flexibility
- ✅ Easy to swap models (Gemini → GPT-4 → Claude)
- ✅ Tool ecosystem
- ✅ Framework standardization

### 4. Maintainability
- ✅ Less custom code
- ✅ Industry-standard patterns
- ✅ Better debugging tools

## Risks & Mitigation

### Risk 1: Breaking Changes
**Mitigation:** Run both implementations in parallel initially, A/B test

### Risk 2: Performance Degradation
**Mitigation:** Benchmark thoroughly before full rollout

### Risk 3: Additional Dependencies
**Mitigation:** Review LiteLLM and OpenAI Agents SDK for security/stability

### Risk 4: Learning Curve
**Mitigation:** Document patterns, create examples

## Code Examples

### Current Implementation
```python
# Current: Direct Gemini API call
response = await gemini_client.generate_content(
    model="gemini-2.0-flash",
    contents=[{"role": "user", "parts": [{"text": query}]}]
)
```

### New Implementation
```python
# New: OpenAI Agents SDK with Gemini via LiteLLM
result = await Runner.run(
    textbook_agent,
    query,
    config=run_config
)
```

## Resources

### Documentation
- [OpenAI Agents Python SDK](https://github.com/openai/openai-agents-python)
- [LiteLLM Documentation](https://docs.litellm.ai/)
- [Context7 SDK Docs](/openai/openai-agents-python)

### Code Snippets Retrieved
```python
# Using Gemini with OpenAI Agents SDK
from agents import Agent
from agents.extensions.models.litellm_model import LitellmModel

gemini_agent = Agent(
    name="Gemini Assistant",
    model=LitellmModel(
        model="gemini/gemini-2.0-flash",
        api_key="your-gemini-key"
    )
)

# Or shorthand
gemini_agent = Agent(model="litellm/gemini/gemini-2.5-flash", ...)
```

## Success Metrics

- [ ] All existing functionality works
- [ ] Response quality maintained or improved
- [ ] Response time < 3 seconds (p95)
- [ ] Zero breaking changes to frontend
- [ ] 100% test coverage for new agent service
- [ ] Successful deployment to Hugging Face

## Next Steps

When ready to implement:

1. **Create a feature branch:**
   ```bash
   git checkout -b feature/openai-agents-sdk
   ```

2. **Run the implementation command:**
   ```bash
   /sp.implement
   ```

3. **Follow the task breakdown in this document**

4. **Test thoroughly before merging**

## Related Documents

- Current Chat API: `backend/src/api/chat.py`
- Current Gemini Service: `backend/src/services/generation.py`
- Qdrant Client: `backend/src/services/qdrant_client.py`
- Frontend ChatWidget: `frontend/my-website/src/components/ChatWidget/ChatWidget.tsx`

## Notes

- Keep this document updated as requirements change
- Add learnings from implementation to this doc
- Consider creating a migration checklist when starting
- May want to create separate agents for different purposes:
  - **Textbook Agent** - Answers course questions
  - **Translator Agent** - Translates to Urdu
  - **Tutor Agent** - Provides step-by-step explanations
  - **Triage Agent** - Routes to appropriate sub-agent

---

**Last Updated:** 2025-12-01
**Assigned To:** TBD
**Blocked By:** None
**Blocks:** Multi-agent features, advanced conversation features
