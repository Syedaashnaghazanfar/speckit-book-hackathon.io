# Technology Research: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-11-28
**Phase**: 0 (Research & Technology Validation)
**Status**: Complete

## Overview

This document consolidates research findings for the hackathon-mandated technology stack. All technologies are fixed requirements and cannot be changed.

---

## 1. Docusaurus 3.x Purple/Neon Theming

### Decision
Use **Custom CSS Variables** approach with `src/css/custom.css`

### Rationale
- Simpler than creating a full custom theme plugin
- Docusaurus 3.x provides comprehensive CSS variable support
- Faster iteration during hackathon timeline
- Easier to maintain and debug

### Implementation Pattern
```css
/* src/css/custom.css */
:root {
  /* Purple/Neon Color Palette */
  --ifm-color-primary: #9333EA;        /* Purple 600 */
  --ifm-color-primary-dark: #7E22CE;   /* Purple 700 */
  --ifm-color-primary-darker: #6B21A8; /* Purple 800 */
  --ifm-color-primary-darkest: #581C87; /* Purple 900 */
  --ifm-color-primary-light: #A855F7;  /* Purple 500 */
  --ifm-color-primary-lighter: #C084FC; /* Purple 400 */
  --ifm-color-primary-lightest: #D8B4FE; /* Purple 300 */

  /* Neon Accents */
  --neon-pink: #FF006E;
  --neon-cyan: #00F5FF;
  --neon-green: #39FF14;

  /* Dark Theme Overrides */
  --ifm-background-color: #0F0A1A;
  --ifm-navbar-background-color: #1A0F2E;
  --ifm-card-background-color: #1F1635;
}

.neon-glow {
  box-shadow: 0 0 10px var(--neon-pink), 0 0 20px var(--neon-pink);
}
```

### Alternatives Considered
- **Custom Theme Plugin**: Too time-intensive for hackathon
- **Third-party Theme**: Limited purple/neon options, harder to customize

### References
- [Docusaurus Styling Guide](https://docusaurus.io/docs/styling-layout)
- [CSS Variables Documentation](https://developer.mozilla.org/en-US/docs/Web/CSS/Using_CSS_custom_properties)

---

## 2. OpenAI Embedding API Best Practices

### Decision
Batch embeddings at **100 chunks per request** with exponential backoff retry logic

### Rationale
- OpenAI rate limits: 3,000 requests/minute (Tier 1)
- Batching reduces API call overhead
- Exponential backoff handles transient failures gracefully

### Implementation Pattern
```python
# backend/src/services/embeddings.py
import openai
import time
from typing import List

async def generate_embeddings_batch(texts: List[str], batch_size: int = 100) -> List[List[float]]:
    """
    Generate embeddings in batches with retry logic.

    Args:
        texts: List of text chunks (max 8191 tokens each)
        batch_size: Chunks per API request (max 100)

    Returns:
        List of embedding vectors (1536 dimensions each)
    """
    all_embeddings = []

    for i in range(0, len(texts), batch_size):
        batch = texts[i:i + batch_size]

        for attempt in range(3):  # Max 3 retries
            try:
                response = await openai.Embedding.acreate(
                    model="text-embedding-3-small",
                    input=batch
                )
                all_embeddings.extend([item['embedding'] for item in response['data']])
                break
            except openai.error.RateLimitError:
                wait_time = 2 ** attempt  # Exponential backoff: 1s, 2s, 4s
                time.sleep(wait_time)
            except Exception as e:
                print(f"Embedding generation failed: {e}")
                raise

    return all_embeddings
```

### Chunk Size Strategy
- **500 tokens per chunk** with **100-token overlap**
- Rationale: Balance between context preservation and API efficiency
- Estimated total chunks: 500-1000 for full textbook

### Error Handling
- `RateLimitError`: Exponential backoff retry
- `InvalidRequestError`: Log and skip malformed chunks
- `APIConnectionError`: Retry with fresh connection

### References
- [OpenAI Embedding Guide](https://platform.openai.com/docs/guides/embeddings)
- [text-embedding-3-small Model](https://platform.openai.com/docs/models/embeddings)

---

## 3. Qdrant Cloud Setup & Connection Patterns

### Decision
Use **Qdrant Cloud Free Tier** with HNSW indexing for vector search

### Rationale
- Free tier: 1GB storage (sufficient for 500-1000 chunks × 1536 dimensions)
- Managed service eliminates infrastructure overhead
- Sub-500ms query latency with HNSW algorithm

### Implementation Pattern
```python
# backend/src/services/qdrant_client.py
from qdrant_client import QdrantClient
from qdrant_client.models import Distance, VectorParams, PointStruct
import os

client = QdrantClient(
    url=os.getenv("QDRANT_URL"),  # e.g., https://xyz.qdrant.io
    api_key=os.getenv("QDRANT_API_KEY")
)

# Create collection (one-time setup)
client.recreate_collection(
    collection_name="textbook_embeddings",
    vectors_config=VectorParams(size=1536, distance=Distance.COSINE)
)

# Insert embeddings
points = [
    PointStruct(
        id=chunk_id,
        vector=embedding_vector,
        payload={
            "module": "Module 1: ROS 2",
            "week": 3,
            "section": "Nodes and Topics",
            "content": original_text
        }
    )
    for chunk_id, embedding_vector, original_text in chunks
]
client.upsert(collection_name="textbook_embeddings", points=points)

# Query similar chunks
search_results = client.search(
    collection_name="textbook_embeddings",
    query_vector=query_embedding,
    limit=5  # Top 5 most relevant chunks
)
```

### Metadata Schema
```json
{
  "module": "String (e.g., 'Module 1: ROS 2')",
  "week": "Integer (1-13)",
  "section": "String (e.g., 'Nodes and Topics')",
  "chapter_id": "UUID",
  "chunk_id": "Integer",
  "content": "String (original text for citation)"
}
```

### References
- [Qdrant Cloud Docs](https://qdrant.tech/documentation/cloud/)
- [HNSW Algorithm](https://qdrant.tech/articles/filtrable-hnsw/)

---

## 4. FastAPI + Gemini MCP Integration

### Decision
Use **Google Generative AI SDK** with **Context-7 MCP** server for RAG-only responses

### Rationale
- Gemini models support long context windows (up to 32k tokens)
- Temperature=0.3 for factual, deterministic responses
- MCP provides structured context management

### Implementation Pattern
```python
# backend/src/services/gemini_chat.py
import google.generativeai as genai
from typing import List, Dict

genai.configure(api_key=os.getenv("GEMINI_API_KEY"))

async def generate_rag_response(
    user_query: str,
    retrieved_chunks: List[Dict]
) -> str:
    """
    Generate RAG response using Gemini with strict context adherence.

    Args:
        user_query: User's question
        retrieved_chunks: Top-k chunks from Qdrant with metadata

    Returns:
        Generated response with citations
    """
    # Build context from retrieved chunks
    context = "\n\n".join([
        f"[Module: {chunk['module']}, Week: {chunk['week']}, Section: {chunk['section']}]\n{chunk['content']}"
        for chunk in retrieved_chunks
    ])

    system_prompt = f"""You are a helpful teaching assistant for a Physical AI & Humanoid Robotics textbook.

CRITICAL RULES:
1. Answer ONLY using the provided context below. Do NOT use external knowledge.
2. If the context does not contain the answer, respond with: "This information is not found in the book content."
3. ALWAYS cite your sources in the format: [Source: Module X, Week Y, Section Z]
4. Be concise but accurate. Use technical terminology when appropriate.

CONTEXT:
{context}

USER QUESTION: {user_query}

ANSWER (with citations):"""

    model = genai.GenerativeModel('gemini-pro')
    response = await model.generate_content_async(
        system_prompt,
        generation_config=genai.types.GenerationConfig(
            temperature=0.3,  # Low temperature for factual responses
            max_output_tokens=500
        )
    )

    return response.text
```

### RAG-Only Enforcement Strategy
1. **System Prompt**: Explicit instructions to use only provided context
2. **Low Temperature**: 0.3 (reduces hallucination probability)
3. **Citation Validation**: Backend verifies citations match retrieved chunks
4. **Context Window**: Limit to top-5 chunks (prevents information overload)

### References
- [Gemini API Documentation](https://ai.google.dev/docs)
- [Context-7 MCP Protocol](https://modelcontextprotocol.io/)

---

## 5. ChatKit SDK Embedding in Docusaurus

### Decision
Embed **ChatKit React Component** as a floating widget using Docusaurus swizzling

### Rationale
- ChatKit provides pre-built UI components (message history, input box, typing indicators)
- Swizzling allows custom integration without forking Docusaurus
- Floating widget maintains visibility across all pages

### Implementation Pattern
```typescript
// frontend/src/components/ChatWidget.tsx
import React, { useState } from 'react';
import { ChatContainer, MessageList, Message, MessageInput } from '@chatkit/react';

interface ChatWidgetProps {
  apiEndpoint: string;
}

export const ChatWidget: React.FC<ChatWidgetProps> = ({ apiEndpoint }) => {
  const [messages, setMessages] = useState<Message[]>([]);
  const [isMinimized, setIsMinimized] = useState(false);

  const handleSendMessage = async (text: string) => {
    const userMessage: Message = { role: 'user', content: text };
    setMessages([...messages, userMessage]);

    const response = await fetch(`${apiEndpoint}/api/chat`, {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify({ message: text, session_id: sessionStorage.getItem('chat_session_id') })
    });

    const data = await response.json();
    const assistantMessage: Message = { role: 'assistant', content: data.response };
    setMessages([...messages, userMessage, assistantMessage]);
  };

  return (
    <div className={`chat-widget ${isMinimized ? 'minimized' : ''}`}>
      <button onClick={() => setIsMinimized(!isMinimized)}>
        {isMinimized ? 'Open Chat' : 'Minimize'}
      </button>
      {!isMinimized && (
        <ChatContainer>
          <MessageList messages={messages} />
          <MessageInput onSendMessage={handleSendMessage} />
        </ChatContainer>
      )}
    </div>
  );
};
```

### Docusaurus Integration
```javascript
// docusaurus.config.js
module.exports = {
  // ...
  themeConfig: {
    // ...
  },
  plugins: [
    [
      '@docusaurus/plugin-client-redirects',
      {
        // Custom plugin to inject ChatWidget globally
        inject: () => '<ChatWidget apiEndpoint={process.env.REACT_APP_API_URL} />'
      }
    ]
  ]
};
```

### References
- [ChatKit Documentation](https://chatkit.io/docs)
- [Docusaurus Swizzling Guide](https://docusaurus.io/docs/swizzling)

---

## 6. Better-Auth + Neon Postgres Integration (Bonus)

### Decision
Use **Better-Auth** library with **Neon Postgres adapter** for user authentication

### Rationale
- Better-Auth provides built-in email/password flows
- Neon Postgres free tier: 10GB storage, serverless (pay-per-request)
- Seamless integration with FastAPI via asyncpg driver

### Implementation Pattern
```python
# backend/src/services/auth_service.py
from better_auth import BetterAuth
from asyncpg import create_pool

auth = BetterAuth(
    database_url=os.getenv("NEON_DATABASE_URL"),
    secret_key=os.getenv("AUTH_SECRET_KEY")
)

async def signup_user(email: str, password: str, profile_data: Dict) -> Dict:
    """
    Create new user with profile data.

    Returns:
        { user_id: UUID, session_token: str }
    """
    user = await auth.signup(email=email, password=password)

    # Store additional profile data
    async with create_pool(os.getenv("NEON_DATABASE_URL")) as pool:
        await pool.execute(
            "INSERT INTO user_profiles (user_id, programming_experience, hardware_familiarity) VALUES ($1, $2, $3)",
            user.id, profile_data['programming_experience'], profile_data['hardware_familiarity']
        )

    session_token = await auth.create_session(user.id)
    return {"user_id": user.id, "session_token": session_token}
```

### Database Schema (Neon Postgres)
```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    user_id UUID UNIQUE NOT NULL,
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    programming_experience VARCHAR(20) CHECK (programming_experience IN ('beginner', 'intermediate', 'advanced')),
    hardware_familiarity VARCHAR(20) CHECK (hardware_familiarity IN ('none', 'some', 'extensive')),
    preferred_language VARCHAR(2) DEFAULT 'en' CHECK (preferred_language IN ('en', 'ur')),
    created_at TIMESTAMP DEFAULT NOW()
);

CREATE INDEX idx_user_email ON user_profiles(email);
```

### References
- [Better-Auth Documentation](https://better-auth.com/docs)
- [Neon Postgres Docs](https://neon.tech/docs)

---

## 7. Text Selection Capture in React/MDX

### Decision
Use **`window.getSelection()` API** with custom React hook `useTextSelection`

### Rationale
- Native browser API (no external dependencies)
- Works seamlessly with MDX content
- Lightweight and performant

### Implementation Pattern
```typescript
// frontend/src/hooks/useTextSelection.ts
import { useEffect, useState } from 'react';

export const useTextSelection = () => {
  const [selectedText, setSelectedText] = useState('');

  useEffect(() => {
    const handleSelectionChange = () => {
      const selection = window.getSelection();
      setSelectedText(selection?.toString() || '');
    };

    document.addEventListener('selectionchange', handleSelectionChange);
    return () => document.removeEventListener('selectionchange', handleSelectionChange);
  }, []);

  return selectedText;
};

// Usage in component
const TextSelectionButton = () => {
  const selectedText = useTextSelection();

  if (!selectedText) return null;

  return (
    <button className="ask-about-this" onClick={() => {
      // Send selectedText to /api/chat/selection
    }}>
      Ask about this
    </button>
  );
};
```

### Mobile Support
- **Long-press gesture**: Native browser behavior triggers `selectionchange` event
- **Floating Action Button (FAB)**: Position button near selection using `Range.getBoundingClientRect()`

### References
- [Selection API MDN](https://developer.mozilla.org/en-US/docs/Web/API/Selection)
- [React Hooks Guide](https://react.dev/reference/react)

---

## 8. RTL CSS Support for Urdu Translation (Bonus)

### Decision
Use **CSS `dir="rtl"` attribute** with selective LTR overrides for code blocks

### Rationale
- Native CSS support (no JavaScript manipulation required)
- Preserves code block readability (LTR)
- Minimal performance overhead

### Implementation Pattern
```css
/* frontend/src/css/custom.css */
.rtl-content {
  direction: rtl;
  text-align: right;
}

.rtl-content code,
.rtl-content pre {
  direction: ltr;  /* Override for code blocks */
  text-align: left;
}

.rtl-content .technical-term {
  direction: ltr;  /* Keep technical terms in LTR */
  display: inline-block;
}
```

```typescript
// frontend/src/components/TranslateButton.tsx
const TranslateButton = ({ chapterId }: { chapterId: string }) => {
  const [isUrdu, setIsUrdu] = useState(false);

  const handleTranslate = async () => {
    const response = await fetch(`/api/translate`, {
      method: 'POST',
      body: JSON.stringify({ chapter_id: chapterId, target_language: 'ur' })
    });
    const { translated_content } = await response.json();

    // Apply RTL class to content container
    document.getElementById('chapter-content')?.classList.add('rtl-content');
    setIsUrdu(true);
  };

  return <button onClick={handleTranslate}>Translate to Urdu</button>;
};
```

### Technical Term Preservation
- Backend regex: `/(ROS 2|URDF|Gazebo|Isaac|VLA|Python|C\+\+)/g`
- Wrap matches in `<span class="technical-term">` during translation

### References
- [CSS Writing Modes](https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_Writing_Modes)
- [RTL Best Practices](https://www.w3.org/International/questions/qa-html-dir)

---

## Summary of Validated Technologies

| Technology | Status | Rationale |
|------------|--------|-----------|
| Docusaurus 3.x | ✅ Validated | Custom CSS variables for purple/neon theme |
| OpenAI Embeddings | ✅ Validated | Batch processing at 100 chunks/request |
| Qdrant Cloud | ✅ Validated | Free tier sufficient, HNSW indexing for speed |
| FastAPI | ✅ Validated | Async support, auto-generated OpenAPI docs |
| Gemini + MCP | ✅ Validated | Temperature=0.3 for RAG-only responses |
| ChatKit SDK | ✅ Validated | React integration via swizzling |
| Better-Auth | ✅ Validated | Neon Postgres adapter for user profiles |
| Text Selection | ✅ Validated | Native `window.getSelection()` API |
| RTL CSS | ✅ Validated | `dir="rtl"` with LTR code block overrides |

**All research tasks complete. Ready for Phase 1: Data Model & Contracts.**
