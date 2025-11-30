# Implementation Plan: Physical AI & Humanoid Robotics Textbook

**Branch**: `001-physical-ai-textbook` | **Date**: 2025-11-28 | **Spec**: [spec.md](./spec.md)
**Input**: Feature specification from `/specs/001-physical-ai-textbook/spec.md`

## Summary

Build an AI-native, interactive textbook with 4 modules across 13 weeks, featuring a RAG chatbot that answers exclusively from book embeddings. The system uses Docusaurus for the frontend, FastAPI for the backend, OpenAI for embeddings, Qdrant for vector storage, and Gemini (via Context-7 MCP) for chat responses. Bonus features include Better-Auth authentication, content personalization, and Urdu translation.

**Technical Approach**: Hybrid architecture with static site generation (Docusaurus) for content delivery and a serverless backend (FastAPI) for RAG, auth, and dynamic features. Content is pre-processed into embeddings during build time and queried at runtime via Qdrant vector search.

## Technical Context

**Language/Version**: Python 3.11+ (backend), TypeScript 5.x (frontend), Node.js 18+ (Docusaurus build)
**Primary Dependencies**:
- Frontend: Docusaurus 3.x, React 18.2, ChatKit SDK, Better-Auth
- Backend: FastAPI 0.110+, Pydantic 2.5+, Qdrant Client 1.7+, OpenAI SDK 1.12+, Google Generative AI 0.3+
**Storage**:
- Vector DB: Qdrant Cloud (Free Tier, 1GB limit)
- Relational DB: Neon Serverless Postgres (for user profiles - bonus feature)
- Static Assets: GitHub Pages / Netlify
**Testing**:
- Frontend: Jest + React Testing Library
- Backend: pytest with async support
- Integration: Playwright for E2E tests
**Target Platform**: Web (desktop + mobile responsive), deployed as static site + serverless backend
**Project Type**: Web application (separate frontend/backend)
**Performance Goals**:
- Page load: <2s (p95)
- RAG response: <3s (p95)
- Embedding generation: <30min for full book
- Vector search: <500ms per query
**Constraints**:
- Qdrant Free Tier: 1GB storage limit
- OpenAI rate limits: Batch embeddings at 100 chunks/request
- Build time: <5 minutes for `npm run build`
- Hackathon deadline: Nov 30, 2025 6:00 PM
**Scale/Scope**:
- Content: 4 modules, 13 weeks, ~50-100 pages of MDX content
- Concurrent users: 100 without degradation
- Embedding chunks: Estimated 500-1000 chunks (500 tokens each)

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

### Principle I: User Experience First ✅
- **Purple/Neon Theme**: Custom Docusaurus theme with CSS variables
- **Mobile Responsive**: Docusaurus built-in responsiveness + custom breakpoints (320px-2560px)
- **WCAG 2.1 AA**: Automated testing with axe-core, manual validation
- **Lazy Loading**: Docusaurus supports image lazy loading via MDX
- **Code Splitting**: Webpack/Vite code splitting configured in Docusaurus

**Compliance**: PASS

### Principle II: Educational Excellence ✅
- **Progressive Complexity**: Content structure enforced via folder organization (Week 1-2 → Week 13)
- **Runnable Examples**: Syntax highlighting via Prism, copy-to-clipboard via custom component
- **Visual Learning**: Images embedded in MDX, diagrams stored as PNG/SVG
- **Assessments**: Self-check questions in dedicated MDX sections per week

**Compliance**: PASS

### Principle III: RAG-Only Answering (CRITICAL) ✅
- **Strict Retrieval**: System prompt enforces no external knowledge; Gemini model temperature=0.3
- **Text Selection Mode**: Custom JavaScript hook captures selection, sends scoped query to backend
- **Explicit "Not Found"**: Backend returns 404-like structure when no relevant chunks found
- **Citation Format**: Backend metadata includes chapter/section/module; formatted in response template

**Compliance**: PASS

### Principle IV: Technical Stack Immutability ✅
| Component | Specified Technology | Implementation Plan |
|-----------|---------------------|---------------------|
| Book Framework | Docusaurus 3.x | ✅ Package.json: `@docusaurus/core: ^3.0.0` |
| Theme | Purple + Neon Custom | ✅ Custom CSS file: `src/css/custom.css` |
| Embeddings | OpenAI (text-embedding-3-small) | ✅ OpenAI SDK with model parameter |
| Vector DB | Qdrant Cloud (Free Tier) | ✅ Qdrant Client with cloud endpoint |
| Backend | FastAPI | ✅ FastAPI 0.110+ |
| Agent LLM | Gemini via Context-7 MCP | ✅ Google Generative AI SDK + MCP integration |
| Chat UI | ChatKit SDK | ✅ ChatKit React component |
| Auth (Bonus) | Better-Auth | ✅ Better-Auth library |
| Database | Neon Serverless Postgres | ✅ asyncpg driver |

**Compliance**: PASS

### Principle V: Code Quality Standards ✅
- **TypeScript Strict Mode**: `tsconfig.json` with `"strict": true`
- **Python Type Hints**: All FastAPI route handlers and service functions annotated
- **Black Formatting**: Pre-commit hook configured
- **Unit Tests**: pytest for backend (embedding pipeline, API routes); Jest for frontend
- **OpenAPI/Swagger**: FastAPI auto-generates docs at `/docs`

**Compliance**: PASS

### Principle VI: Security Principles ✅
- **API Keys**: `.env` files gitignored; loaded via `python-dotenv` and `process.env`
- **Rate Limiting**: FastAPI middleware (`slowapi`) limiting 100 req/min per IP
- **Input Sanitization**: Pydantic validation on all request bodies
- **CORS**: FastAPI CORS middleware with production origin whitelist

**Compliance**: PASS

### Principle VII: Performance Requirements ✅
- **Batch Embedding**: OpenAI API batched at 100 chunks/request max
- **RAG Latency**: Async FastAPI + connection pooling for <3s p95
- **Build Time**: Docusaurus optimizations (static generation, incremental builds)
- **Vector Search**: Qdrant's HNSW index for <500ms queries

**Compliance**: PASS

**GATE DECISION**: ✅ ALL PRINCIPLES SATISFIED - Proceed to Phase 0

## Project Structure

### Documentation (this feature)

```text
specs/001-physical-ai-textbook/
├── plan.md              # This file (/sp.plan command output)
├── research.md          # Phase 0 output (technology research and best practices)
├── data-model.md        # Phase 1 output (entity schemas and relationships)
├── quickstart.md        # Phase 1 output (developer setup guide)
├── contracts/           # Phase 1 output (API endpoint specs)
│   ├── chat.openapi.yaml
│   ├── auth.openapi.yaml
│   └── personalization.openapi.yaml
└── tasks.md             # Phase 2 output (/sp.tasks command - NOT created by /sp.plan)
```

### Source Code (repository root)

```text
# Option 2: Web application (frontend + backend)

backend/
├── src/
│   ├── main.py                 # FastAPI application entry point
│   ├── config.py               # Environment configuration
│   ├── models/                 # Pydantic models
│   │   ├── chat.py
│   │   ├── user.py
│   │   └── embedding.py
│   ├── services/               # Business logic
│   │   ├── embeddings.py       # OpenAI embedding generation
│   │   ├── qdrant_client.py    # Vector DB operations
│   │   ├── gemini_chat.py      # Gemini + Context-7 MCP integration
│   │   ├── auth_service.py     # Better-Auth integration (bonus)
│   │   └── personalization.py  # Gemini personalization (bonus)
│   ├── api/                    # API routes
│   │   ├── chat.py             # /api/chat endpoints
│   │   ├── auth.py             # /api/auth endpoints (bonus)
│   │   └── health.py           # /api/health
│   └── middleware/             # Middleware (CORS, rate limiting, error handling)
│       ├── cors.py
│       ├── rate_limit.py
│       └── error_handler.py
├── tests/
│   ├── unit/                   # Unit tests for services
│   ├── integration/            # API endpoint tests
│   └── contract/               # Contract tests vs OpenAPI specs
├── scripts/
│   └── generate_embeddings.py # One-time embedding generation script
├── requirements.txt
├── pyproject.toml              # Poetry/pip-tools config
└── .env.example

frontend/  (Docusaurus site)
├── docs/                       # MDX content organized by module/week
│   ├── intro.md
│   ├── module-1-ros2/
│   │   ├── week-01-intro.mdx
│   │   ├── week-02-basics.mdx
│   │   └── week-03-nodes.mdx
│   ├── module-2-gazebo/
│   ├── module-3-isaac/
│   └── module-4-vla/
├── src/
│   ├── components/             # React components
│   │   ├── ChatWidget.tsx      # ChatKit integration
│   │   ├── TextSelectionButton.tsx
│   │   ├── PersonalizeButton.tsx
│   │   └── TranslateButton.tsx
│   ├── hooks/                  # Custom React hooks
│   │   ├── useTextSelection.ts
│   │   └── useChatAPI.ts
│   ├── css/
│   │   └── custom.css          # Purple/neon theme
│   └── pages/
│       ├── index.tsx           # Landing page
│       └── auth/
│           ├── signin.tsx
│           └── signup.tsx
├── static/
│   └── img/                    # Images and diagrams
├── docusaurus.config.js
├── sidebars.js
├── package.json
├── tsconfig.json
└── .env.example
```

**Structure Decision**: Web application with separate `frontend/` (Docusaurus) and `backend/` (FastAPI) directories. Frontend is statically built and deployed to GitHub Pages; backend is deployed as a serverless function (e.g., Vercel, AWS Lambda) or containerized (Docker + Fly.io).

## Complexity Tracking

> **No violations detected. All constitution requirements are satisfied by the technical stack and architecture.**

| Principle | Requirement | Justification | Simpler Alternative Rejected Because |
|-----------|-------------|---------------|-------------------------------------|
| N/A | N/A | N/A | N/A |

## Phase 0: Research & Technology Validation

**Objective**: Validate technology choices, resolve unknowns, and document best practices for hackathon tech stack.

**Output**: `research.md` documenting:
1. Docusaurus 3.x purple/neon theming strategies
2. OpenAI embedding API best practices (batch sizes, error handling)
3. Qdrant Cloud setup and connection patterns
4. FastAPI + Gemini MCP integration architecture
5. ChatKit SDK embedding in Docusaurus
6. Better-Auth + Neon Postgres integration patterns (bonus)
7. Text selection capture in React/MDX environments
8. RTL CSS support strategies for Urdu (bonus)

**Research Tasks**:
- ✅ Docusaurus theming: Custom CSS variables vs. custom theme plugin
- ✅ OpenAI API: Batch embedding endpoint usage, rate limit handling
- ✅ Qdrant: Cloud API authentication, collection creation, HNSW indexing
- ✅ Gemini + Context-7 MCP: MCP server setup, prompt engineering for RAG-only responses
- ✅ ChatKit: React integration patterns, session management
- ✅ Better-Auth: Neon Postgres adapter, profile schema design (bonus)

## Phase 1: Design & Contracts

**Objective**: Define data models, API contracts, and developer quickstart guide.

### Data Model Design

**Output**: `data-model.md`

**Entities** (from spec.md):

1. **Module** (Content Entity)
   - `id`: UUID
   - `title`: String (e.g., "The Robotic Nervous System (ROS 2)")
   - `description`: Text
   - `learning_outcomes`: List[String]
   - `order`: Integer (1-4)

2. **Week** (Content Entity)
   - `id`: UUID
   - `week_number`: Integer (1-13)
   - `title`: String
   - `module_id`: UUID (FK to Module)
   - `content_path`: String (MDX file path)

3. **Chapter/Section** (Content Entity)
   - `id`: UUID
   - `title`: String
   - `week_id`: UUID (FK to Week)
   - `content`: Text (MDX content)
   - `position`: Integer
   - `has_code_examples`: Boolean
   - `has_assessments`: Boolean

4. **EmbeddingChunk** (Vector Entity)
   - `id`: UUID
   - `chapter_id`: UUID (FK to Chapter)
   - `content`: Text (original text, 500 tokens)
   - `embedding`: Vector[1536] (OpenAI embedding)
   - `metadata`: JSON
     - `module`: String
     - `week`: Integer
     - `section`: String
     - `page`: Integer
     - `chunk_id`: Integer

5. **ChatSession** (Ephemeral Entity)
   - `session_id`: UUID
   - `user_id`: UUID (nullable, null for anonymous)
   - `created_at`: Timestamp
   - `messages`: List[ChatMessage] (in-memory, not persisted)

6. **ChatMessage** (Ephemeral Entity)
   - `role`: Enum["user", "assistant"]
   - `content`: Text
   - `citations`: List[Citation] (for assistant messages)
   - `timestamp`: Timestamp

7. **Citation** (Nested Entity)
   - `chapter`: String
   - `section`: String
   - `module`: String
   - `relevance`: Float (0.0-1.0)

8. **UserProfile** (Bonus - Persistent Entity)
   - `id`: UUID
   - `email`: String (unique, indexed)
   - `password_hash`: String
   - `programming_experience`: Enum["beginner", "intermediate", "advanced"]
   - `hardware_familiarity`: Enum["none", "some", "extensive"]
   - `preferred_language`: Enum["en", "ur"]
   - `created_at`: Timestamp

9. **PersonalizationRequest** (Bonus - Ephemeral Entity)
   - `user_id`: UUID
   - `chapter_id`: UUID
   - `generated_content`: Text (cached for session)
   - `cache_timestamp`: Timestamp

10. **TranslationCache** (Bonus - Persistent Entity)
    - `chapter_id`: UUID
    - `source_content_hash`: String (SHA-256 of original content)
    - `translated_content`: Text
    - `language`: Enum["ur"]
    - `cached_at`: Timestamp

### API Contracts

**Output**: `contracts/` directory with OpenAPI YAML specs

**Endpoints**:

1. **POST /api/chat**
   - Request: `{ message: string, session_id: string, user_id?: string }`
   - Response: `{ response: string, citations: Citation[], session_id: string }`
   - RAG flow: Query → Qdrant vector search → Gemini prompt with context

2. **POST /api/chat/selection**
   - Request: `{ message: string, selected_text: string, session_id: string }`
   - Response: `{ response: string, context_limited: true, session_id: string }`
   - RAG flow: Hash selection → retrieve embeddings for that specific text → scoped query

3. **GET /api/health**
   - Response: `{ status: "ok", services: { qdrant: "up", gemini: "up" } }`

4. **POST /api/auth/signup** (Bonus)
   - Request: `{ email: string, password: string, programming_experience: string, hardware_familiarity: string }`
   - Response: `{ user_id: string, session_token: string }`

5. **POST /api/auth/signin** (Bonus)
   - Request: `{ email: string, password: string }`
   - Response: `{ user_id: string, session_token: string }`

6. **POST /api/auth/signout** (Bonus)
   - Request: `{ session_token: string }`
   - Response: `{ success: true }`

7. **POST /api/personalize** (Bonus)
   - Request: `{ chapter_id: string, user_id: string }`
   - Response: `{ personalized_content: string }`

8. **POST /api/translate** (Bonus)
   - Request: `{ chapter_id: string, target_language: "ur" }`
   - Response: `{ translated_content: string }`

### Quickstart Guide

**Output**: `quickstart.md`

**Developer Setup Steps**:

1. **Prerequisites**
   - Node.js 18+
   - Python 3.11+
   - Git

2. **Environment Setup**
   - Clone repository
   - Copy `.env.example` to `.env` and fill in:
     - `OPENAI_API_KEY`
     - `QDRANT_API_KEY`
     - `QDRANT_URL`
     - `GEMINI_API_KEY`
     - `NEON_DATABASE_URL` (bonus)

3. **Backend Setup**
   ```bash
   cd backend
   python -m venv venv
   source venv/bin/activate  # Windows: venv\Scripts\activate
   pip install -r requirements.txt
   python scripts/generate_embeddings.py  # One-time setup
   uvicorn src.main:app --reload
   ```

4. **Frontend Setup**
   ```bash
   cd frontend
   npm install
   npm start  # Development server
   npm run build  # Production build
   ```

5. **Testing**
   - Backend: `pytest backend/tests`
   - Frontend: `npm test`
   - E2E: `npx playwright test`

6. **Deployment**
   - Frontend: `npm run build` → Deploy `build/` to GitHub Pages
   - Backend: Deploy to Vercel/Fly.io/AWS Lambda

### Agent Context Update

**Action**: Run `.specify/scripts/bash/update-agent-context.sh claude`

**Updates**:
- Add Docusaurus 3.x, FastAPI, Qdrant, OpenAI, Gemini to agent context
- Document purple/neon theme patterns
- Add RAG-only system prompt template
- Include text selection capture pattern

## Phase 2: Task Breakdown (Not Part of This Command)

**Note**: Task generation is handled by `/sp.tasks` command after planning is complete.

## Deployment Strategy

### Frontend (Docusaurus Static Site)
- **Build**: `npm run build` generates static HTML/CSS/JS in `build/`
- **Host**: GitHub Pages (free, hackathon-appropriate)
- **Custom Domain**: Optional via CNAME
- **CDN**: GitHub Pages built-in CDN

### Backend (FastAPI)
- **Option 1 (Recommended)**: Vercel Serverless Functions
  - Zero-config deployment
  - Auto-scaling
  - Free tier sufficient for hackathon
- **Option 2**: Fly.io Containers
  - Dockerize FastAPI app
  - Free tier with persistent instances
- **Option 3**: AWS Lambda + API Gateway
  - Fully serverless
  - Pay-per-request pricing

### Database
- **Qdrant Cloud**: Free tier (1GB) hosted vector database
- **Neon Postgres** (Bonus): Free tier serverless PostgreSQL for user profiles

### CI/CD
- **GitHub Actions**:
  - Frontend: Build and deploy to GitHub Pages on merge to `main`
  - Backend: Deploy to Vercel/Fly.io on merge to `main`
  - Tests: Run pytest and Jest on PRs

## Risk Mitigation

| Risk | Mitigation Strategy |
|------|---------------------|
| Qdrant Free Tier Limit (1GB) | Optimize chunk size; monitor usage; compress metadata |
| OpenAI Rate Limits | Batch embeddings at 100 chunks/request; implement exponential backoff |
| Gemini API Availability | Cache responses; implement fallback to static "service unavailable" message |
| Tight Deadline (Nov 30) | Prioritize P1 user stories; defer P3 bonus features if necessary |
| Content Quality | Use Educational-Content-Framework skill; review generated content |
| Embedding Generation Time | Run as one-time background job; cache all embeddings |
| ChatKit SDK Integration | Test early; have fallback to custom chat UI if SDK issues arise |

## Next Steps

After planning approval, proceed with:

1. **Run `/sp.tasks`** to generate task breakdown
2. **Create feature branch** (already on `001-physical-ai-textbook`)
3. **Start implementation** following TDD workflow:
   - Red: Write failing tests
   - Green: Implement minimum code to pass
   - Refactor: Optimize and clean up

## Architectural Decision Records (ADR) Candidates

**Significant decisions requiring ADR documentation**:

1. **Hybrid Static + Serverless Architecture**
   - Decision: Docusaurus static frontend + FastAPI serverless backend
   - Rationale: Separates content delivery (fast, cacheable) from dynamic features (RAG, auth)
   - Alternatives: Fully static (no RAG), fully dynamic (slower, more expensive)

2. **Embedding Generation Strategy**
   - Decision: Pre-generate all embeddings during build time
   - Rationale: Faster runtime queries, predictable costs
   - Alternatives: On-demand embedding (slower, higher API costs)

3. **RAG-Only Enforcement Mechanism**
   - Decision: System prompt + temperature=0.3 + citation validation
   - Rationale: Prevents hallucinations, meets hackathon requirement
   - Alternatives: Fine-tuned model (time-intensive), retrieval-only (less flexible)

**Recommendation**: Document these decisions with `/sp.adr` command after planning phase.

---

**Plan Status**: ✅ COMPLETE - Ready for `/sp.tasks`

**Date**: 2025-11-28

**Next Command**: `/sp.tasks` to generate actionable task breakdown
