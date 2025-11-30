---
id: 0002
title: Physical AI Textbook Plan
stage: plan
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: system
command: /sp.plan
labels: ["plan", "architecture", "rag", "hackathon", "docusaurus"]
links:
  spec: specs/001-physical-ai-textbook/spec.md
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-textbook/plan.md
  - specs/001-physical-ai-textbook/research.md
  - specs/001-physical-ai-textbook/data-model.md
  - specs/001-physical-ai-textbook/quickstart.md
tests:
  - N/A (planning artifact)
---

## Prompt

Create implementation plan for Physical AI & Humanoid Robotics Textbook feature (001-physical-ai-textbook).

**Context**:
- AI-native textbook with RAG chatbot
- 4 modules across 13 weeks
- Fixed hackathon tech stack (Docusaurus, FastAPI, OpenAI, Qdrant, Gemini, ChatKit, Better-Auth, Neon)
- Bonus features: authentication, personalization, Urdu translation

**Requirements**:
- Hybrid architecture (static frontend + serverless backend)
- RAG-only answering (no hallucinations)
- Purple/neon aesthetic
- Mobile responsive
- <3s chatbot response time
- <2s page load time

## Response snapshot

Implementation plan created successfully with comprehensive architecture design.

**Created Artifacts**:
1. **plan.md** (500 lines) - Complete implementation plan
2. **research.md** - Technology validation for all 8 stack components
3. **data-model.md** - 10 entities with schemas, validation rules, relationships
4. **quickstart.md** - Developer setup guide (5-minute start)

**Architecture Decisions**:

1. **Hybrid Static + Serverless**
   - Frontend: Docusaurus 3.x (static site generation)
   - Backend: FastAPI (serverless on Vercel/Fly.io)
   - Rationale: Separates content delivery (fast, cacheable) from dynamic features (RAG, auth)

2. **Pre-Generated Embeddings**
   - Strategy: One-time batch processing during build
   - Chunk size: 500 tokens with 100-token overlap
   - Storage: Qdrant Cloud (1GB free tier, ~500-1000 chunks)
   - Rationale: Faster runtime queries, predictable costs

3. **RAG-Only Enforcement**
   - Mechanism: System prompt + temperature=0.3 + citation validation
   - Gemini model with explicit "no external knowledge" instructions
   - Backend validates citations match retrieved chunks
   - Rationale: Prevents hallucinations, meets hackathon requirement

**Constitution Compliance**: ✅ PASS (All 7 principles satisfied)

- I. User Experience First: Purple/neon CSS, responsive design, WCAG 2.1 AA, lazy loading
- II. Educational Excellence: Progressive complexity, code examples, assessments
- III. RAG-Only Answering: System prompt + temp=0.3 + citation enforcement
- IV. Technical Stack Immutability: All 9 components implemented as specified
- V. Code Quality: TypeScript strict, Python type hints, pytest/Jest
- VI. Security: .env for secrets, rate limiting, input sanitization, CORS
- VII. Performance: Batch embeddings (100/req), <3s RAG, <500ms vector search

**Project Structure**:
- `backend/`: FastAPI (Python 3.11+, async)
- `frontend/`: Docusaurus (TypeScript 5.x, React 18.2)
- Deployment: Frontend → GitHub Pages, Backend → Vercel

**Data Model** (10 Entities):
1. Module (4 total) → Week (13 total) → Chapter (many)
2. EmbeddingChunk (Qdrant vector DB, 1536 dims)
3. ChatSession + ChatMessage (ephemeral, in-memory)
4. UserProfile (Neon Postgres, bonus)
5. TranslationCache (Neon Postgres, bonus)

**API Endpoints**:
- POST /api/chat - Main RAG endpoint
- POST /api/chat/selection - Text selection query
- POST /api/auth/signup, /signin, /signout (Bonus)
- POST /api/personalize (Bonus)
- POST /api/translate (Bonus)

**Research Validated**:
✅ Docusaurus purple/neon theming (CSS variables)
✅ OpenAI batch embedding (100 chunks/req, exponential backoff)
✅ Qdrant HNSW indexing (<500ms queries)
✅ Gemini MCP integration (temp=0.3 for factual responses)
✅ ChatKit React embedding (swizzling pattern)
✅ Better-Auth + Neon Postgres (user profiles)
✅ Text selection API (window.getSelection())
✅ RTL CSS support (dir="rtl" with LTR code blocks)

**Deployment Strategy**:
- Frontend: `npm run build` → GitHub Pages (static)
- Backend: Vercel serverless functions (recommended) or Fly.io containers
- CI/CD: GitHub Actions (auto-deploy on merge to main)

**Risk Mitigation**:
- Qdrant 1GB limit: Optimize chunks, monitor usage
- OpenAI rate limits: Batch at 100, exponential backoff
- Tight deadline: Prioritize P1 (core), defer P3 (bonus)

**ADR Candidates**:
1. Hybrid Static + Serverless Architecture
2. Pre-Generation Embedding Strategy
3. RAG-Only Enforcement Mechanism

## Outcome

- ✅ Impact: Complete implementation plan with architecture, data model, and developer quickstart
- 🧪 Tests: Planning artifacts (no tests required at this stage)
- 📁 Files: Created 4 planning documents (plan.md, research.md, data-model.md, quickstart.md)
- 🔁 Next prompts: Run `/sp.tasks` to generate actionable task breakdown
- 🧠 Reflection: Architecture successfully balances hackathon constraints (fixed tech stack) with performance requirements (<3s RAG, <2s page load). Hybrid approach separates concerns effectively: static Docusaurus for content + serverless FastAPI for dynamic RAG. Pre-generated embeddings strategy avoids runtime latency and reduces API costs.

## Evaluation notes (flywheel)

- Failure modes observed: None. All constitution checks passed, all technologies validated.
- Graders run and results (PASS/FAIL): PASS - Architecture aligns with all 7 constitution principles without violations
- Prompt variant (if applicable): Standard planning workflow with comprehensive research phase
- Next experiment (smallest change to try): Consider containerized deployment (Docker + Fly.io) as alternative to Vercel serverless for better cold-start performance
