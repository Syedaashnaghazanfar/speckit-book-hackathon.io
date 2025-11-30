<!--
  SYNC IMPACT REPORT
  ==================
  Version Change: 1.1.0 → 1.2.0

  Modified Principles:
  - Principle IV: Technical Stack Immutability
    - Changed: Embeddings from Gemini (gemini-embedding-001) → FastEmbed (local embedding model)
    - Rationale: Eliminates API rate limiting, improves processing speed, reduces costs, and enables offline operation
  - Principle VII: Performance Requirements
    - Updated: Batch embedding reference changed from Gemini API to FastEmbed local processing
    - Improved: Embedding generation no longer limited by API quotas or network latency

  Added Sections:
  - Amendment History entry for v1.2.0 embedding model change to FastEmbed

  Removed Sections:
  - N/A

  Templates Requiring Updates:
  ✅ plan-template.md - Constitution Check section still aligns with principles
  ✅ spec-template.md - Requirements align with educational excellence and updated technical stack
  ✅ tasks-template.md - Task categorization supports all principles
  ⚠ Backend embedding implementation - Requires code update to use FastEmbed instead of Gemini API
  ⚠ Requirements - Update requirements.txt to include fastembed library
  ⚠ Environment variables - GEMINI_API_KEY no longer required for embeddings (still needed for LLM responses)

  Follow-up TODOs:
  - Update backend/embedding service to use FastEmbed (qdrant-client with fastembed integration)
  - Install fastembed: `pip install fastembed`
  - Remove Gemini API calls for embedding generation (keep Gemini for chat responses only)
  - Update embedding dimension validation (FastEmbed models vary: 384-1024 dims typically)
  - Update Qdrant collection config to match FastEmbed model dimensions
  - Update any documentation referencing Gemini embeddings
-->

# Physical AI & Humanoid Robotics Textbook Constitution

## Core Mission

Build an AI-native, interactive textbook for teaching Physical AI & Humanoid Robotics using
Docusaurus, with an embedded RAG chatbot that answers questions exclusively from book content.

## Core Principles

### I. User Experience First

All UI components MUST adhere to a cohesive purple/neon color scheme. Content MUST be fully
accessible on all devices (mobile responsive). Interactive elements MUST comply with WCAG 2.1
AA accessibility standards. Performance MUST be optimized through lazy loading for images and
code splitting for JavaScript bundles.

**Rationale**: Hackathon aesthetic requirement combined with professional UX standards ensures
the textbook is both visually distinctive and accessible to all learners.

**Non-Negotiable Requirements**:
- Purple + Neon theme applied consistently across all pages and components
- Mobile-first responsive design tested on viewport widths 320px to 2560px
- WCAG 2.1 AA compliance validated via automated and manual testing
- Lazy loading implemented for all images and media assets
- Code splitting configured for JavaScript bundles to optimize initial load time

### II. Educational Excellence

Content MUST flow from fundamental concepts to advanced topics in a progressive manner. Every
concept MUST include runnable code examples where applicable. Visual learning MUST be supported
through diagrams, architecture visuals, and hardware images throughout all modules. Assessment
MUST be integrated with self-check questions in each module.

**Rationale**: Pedagogical best practices ensure effective learning outcomes across diverse
student backgrounds and learning styles.

**Non-Negotiable Requirements**:
- Progressive complexity: Week 1-2 (fundamentals) → Weeks 3-10 (core skills) → Weeks 11-13
  (advanced integration)
- Practical runnable examples for all code-based concepts (ROS 2, Python, simulation)
- Visual aids (diagrams, architecture visuals, photos) included in every major concept section
- Self-assessment questions at the end of each week's content

### III. RAG-Only Answering (CRITICAL)

The chatbot MUST answer ONLY from book embeddings. When users select text, the agent MUST
answer ONLY from that specific selection. If information is not present in embeddings, the
agent MUST explicitly state "not found in book content". Every answer MUST cite the source
chapter and section.

**Rationale**: Prevents hallucination, ensures accuracy, and builds student trust in the
learning material. This is a critical hackathon requirement.

**Non-Negotiable Requirements**:
- Strict retrieval: All responses generated exclusively from embedded book content
- Text selection mode: User-selected text creates scoped RAG queries limited to that content
- Explicit "not found" messages when query cannot be answered from embeddings
- Citation format: Every response must include `[Source: Module X, Week Y, Section Z]`
- No general knowledge responses allowed; agent must refuse to answer out-of-scope questions

### IV. Technical Stack Immutability

The following technology choices are FIXED and MUST NOT be changed under any circumstances:

| Component | Technology | Rationale |
|-----------|-----------|-----------|
| Book Framework | Docusaurus 3.x | Static site generation, MDX support |
| Theme | Purple + Neon Custom | Hackathon aesthetic requirement |
| Embeddings | FastEmbed (Local Model) | Fast, offline, no API limits |
| Vector DB | Qdrant Cloud (Free Tier) | Required by hackathon |
| Backend | FastAPI | Required by hackathon |
| Agent LLM | Gemini Models via Context-7 MCP | Required by hackathon |
| Chat UI | ChatKit SDK | Required by hackathon |
| Auth (Bonus) | Better-Auth | Required for bonus points |
| Database | Neon Serverless Postgres | Required for user data |

**Rationale**: FastEmbed provides local, fast embedding generation without API rate limits or
costs. Gemini Models via Context-7 MCP are still used for LLM responses to meet hackathon
requirements.

### V. Code Quality Standards

TypeScript MUST be used for all frontend code with strict mode enabled. Python backend code
MUST use type hints and Black formatting. Unit tests MUST cover embedding generation and API
endpoints. All public APIs MUST be documented with OpenAPI/Swagger specifications.

**Rationale**: Professional code quality ensures maintainability, readability, and reduces bugs
in a complex multi-technology stack.

**Non-Negotiable Requirements**:
- TypeScript strict mode: `"strict": true` in tsconfig.json
- Python type hints: All function signatures must include type annotations
- Black formatting: Applied to all Python files with default configuration
- Unit test coverage: Minimum viable tests for embedding pipeline and all FastAPI routes
- OpenAPI/Swagger: Auto-generated documentation exposed at `/docs` endpoint

### VI. Security Principles

API keys MUST NEVER be exposed in frontend code; environment variables MUST be used for all
secrets. Rate limiting MUST be implemented on all API endpoints. All user inputs MUST be
sanitized before processing. CORS policies MUST enforce strict origin restrictions in production.

**Rationale**: Protects API quotas, prevents abuse, and safeguards user data in a public-facing
educational application.

**Non-Negotiable Requirements**:
- API keys stored in `.env` files (gitignored) and accessed via `process.env` or `os.getenv()`
- Rate limiting: FastAPI middleware limiting requests to 100/minute per IP for chat endpoints
- Input validation: All user queries sanitized to prevent injection attacks
- CORS: Production deployment permits only the deployed domain origin

### VII. Performance Requirements

Embedding generation MUST use FastEmbed local models for instant processing without API calls.
RAG response time MUST be under 3 seconds for typical queries. Book build time MUST be under 5
minutes for full static build. Vector search queries MUST complete in under 500ms.

**Rationale**: Local embedding generation eliminates network latency and API rate limits,
ensuring fast, reliable performance for hackathon demos.

**Non-Negotiable Requirements**:
- Local embedding: FastEmbed processes all text locally with no external API calls
- RAG latency: p95 response time < 3 seconds (measured from query submission to response display)
- Build time: `npm run build` completes in < 5 minutes on standard hardware
- Vector search: Qdrant similarity queries return results in < 500ms
- Batch processing: FastEmbed can process chunks in parallel without rate limiting concerns

## Content Architecture

### Module Structure (From Course Syllabus)

The textbook MUST be organized into 4 primary modules:

1. **Module 1: The Robotic Nervous System (ROS 2)**
2. **Module 2: The Digital Twin (Gazebo & Unity)**
3. **Module 3: The AI-Robot Brain (NVIDIA Isaac™)**
4. **Module 4: Vision-Language-Action (VLA)**

### Weekly Breakdown

Content MUST be structured across 13 weeks as follows:

- **Weeks 1-2**: Introduction to Physical AI
- **Weeks 3-5**: ROS 2 Fundamentals
- **Weeks 6-7**: Robot Simulation with Gazebo
- **Weeks 8-10**: NVIDIA Isaac Platform
- **Weeks 11-12**: Humanoid Robot Development
- **Week 13**: Conversational Robotics + Capstone Project

## Bonus Feature Governance

### Authentication (50 points)

- Better-Auth implementation for signup/signin
- User profiling questions at signup (software/hardware background assessment)
- Profile data stored in Neon Postgres with proper schema design

### Personalization (50 points)

- Per-chapter personalization button available on every content page
- Uses user profile data to adjust content complexity dynamically
- Gemini model generates personalized explanations based on user background

### Urdu Translation (50 points)

- Per-chapter translation button available on every content page
- Gemini model translates content to Urdu with technical term preservation
- RTL (Right-to-Left) CSS support implemented for proper Urdu text rendering

## Subagent Architecture (For Bonus Points)

### Orchestrator Pattern

Main Claude Code agent MUST delegate to specialized subagents following this pattern:

- **Content Writer Subagent**: Writes chapter markdown following educational framework
- **Embedding Generator Subagent**: Processes markdown text into FastEmbed embeddings
- **Theme Stylist Subagent**: Makes CSS/styling decisions adhering to purple/neon palette
- **API Builder Subagent**: Creates FastAPI endpoint implementations
- **Chatbot Integrator Subagent**: Wires ChatKit SDK with RAG backend

### Handoff Protocol

Main Agent → Recognize Task → Launch Subagent → Isolated Context → Complete Task → Return
Results → Main Agent Proceeds

Each subagent MUST operate in isolation with clear input/output contracts. Results MUST be
validated by the main agent before proceeding to the next step.

## Acceptance Criteria (Definition of Done)

### Base Requirements (100 points)

- [ ] Docusaurus book with all 4 modules + 13 weeks of content published
- [ ] Purple/neon theme applied consistently across all pages
- [ ] FastEmbed embeddings generated for all content and stored
- [ ] Qdrant Cloud vector database populated with all embeddings
- [ ] FastAPI backend with RAG endpoints operational
- [ ] Gemini model answering via Context-7 MCP integration
- [ ] ChatKit embedded and functional on all content pages
- [ ] Text selection triggers focused RAG queries scoped to selection
- [ ] Deployed to GitHub Pages with custom domain (if available)

### Bonus Requirements (Up to 200 additional points)

- [ ] Better-Auth signup/signin with user profiling implemented
- [ ] Per-chapter personalization working and tested
- [ ] Per-chapter Urdu translation working with RTL support
- [ ] Subagent skills documented and reusable for future projects

## Governance

This constitution supersedes all other development practices and decisions. Any amendments to
this constitution MUST be documented with rationale, require explicit approval, and include a
migration plan if applicable.

All pull requests, code reviews, and architectural decisions MUST verify compliance with these
principles. Complexity that violates principles MUST be explicitly justified in the
implementation plan. Development guidance during runtime is provided in `CLAUDE.md` for agent
workflows.

**Amendment Procedure**:
1. Propose amendment with rationale and impact analysis
2. Document in Sync Impact Report
3. Update version number following semantic versioning
4. Propagate changes to dependent templates (plan, spec, tasks)
5. Commit with descriptive message referencing version change

**Version**: 1.2.0 | **Ratified**: 2025-11-28 | **Last Amended**: 2025-11-30

## Amendment History

| Date | Amendment | Rationale |
|------|-----------|-----------|
| 2025-11-28 | Initial constitution (v1.0.0) | Project kickoff for hackathon submission |
| 2025-11-29 | Embedding model change to Gemini (v1.1.0) | Switched from OpenAI text-embedding-3-small to Gemini gemini-embedding-001 per hackathon requirements |
| 2025-11-30 | Embedding model change to FastEmbed (v1.2.0) | Switched from Gemini API to FastEmbed local model to eliminate API rate limits, improve speed, reduce costs, and enable offline operation |
