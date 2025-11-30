---
id: 0001
title: Initial Project Constitution
stage: constitution
date: 2025-11-28
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: master
user: system
command: /sp.constitution
labels: ["constitution", "project-setup", "governance", "hackathon"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A
---

## Prompt

Project Constitution: Physical AI & Humanoid Robotics Textbook

Core Mission:
Build an AI-native, interactive textbook for teaching Physical AI & Humanoid Robotics using Docusaurus, with an embedded RAG chatbot that answers questions exclusively from book content.

Governing Principles:

1. User Experience First
   - Purple + Neon Aesthetic: All UI components must adhere to a cohesive purple/neon color scheme
   - Mobile Responsive: Content must be fully accessible on all devices
   - Accessibility: WCAG 2.1 AA compliance for all interactive elements
   - Fast Load Times: Lazy loading for images, code splitting for JS bundles

2. Educational Excellence
   - Progressive Complexity: Content flows from fundamentals to advanced topics
   - Practical Examples: Every concept includes runnable code examples where applicable
   - Visual Learning: Diagrams, architecture visuals, and hardware images throughout
   - Assessment Integration: Each module includes self-check questions

3. RAG-Only Answering (Critical)
   - Strict Retrieval: The chatbot MUST answer ONLY from book embeddings
   - Text Selection Mode: When user selects text, agent answers ONLY from that selection
   - No Hallucination: If information is not in embeddings, agent admits "not found in book"
   - Citation Required: Every answer must cite the source chapter/section

4. Technical Stack Immutability
   These choices are FIXED and cannot be changed:
   - Book Framework: Docusaurus 3.x
   - Theme: Purple + Neon Custom
   - Embeddings: OpenAI API (text-embedding-3-small)
   - Vector DB: Qdrant Cloud (Free Tier)
   - Backend: FastAPI
   - Agent LLM: Gemini Models via Context-7 MCP
   - Chat UI: ChatKit SDK
   - Auth (Bonus): Better-Auth
   - Database: Neon Serverless Postgres

5. Code Quality Standards
   - TypeScript for Frontend: Strict mode enabled
   - Python for Backend: Type hints required, Black formatting
   - Testing: Unit tests for embedding generation, API endpoints
   - Documentation: All public APIs documented with OpenAPI/Swagger

6. Security Principles
   - API Keys: Never exposed in frontend, use environment variables
   - Rate Limiting: Implement on all API endpoints
   - Input Validation: Sanitize all user inputs before processing
   - CORS: Strict origin policies for production

7. Performance Requirements
   - Embedding Generation: Batch processing, max 100 chunks per request
   - RAG Response Time: < 3 seconds for typical queries
   - Book Build Time: < 5 minutes for full static build
   - Vector Search: < 500ms for similarity queries

Content Architecture:
- Module 1: The Robotic Nervous System (ROS 2)
- Module 2: The Digital Twin (Gazebo & Unity)
- Module 3: The AI-Robot Brain (NVIDIA Isaac™)
- Module 4: Vision-Language-Action (VLA)

Weekly Breakdown:
- Weeks 1-2: Introduction to Physical AI
- Weeks 3-5: ROS 2 Fundamentals
- Weeks 6-7: Robot Simulation with Gazebo
- Weeks 8-10: NVIDIA Isaac Platform
- Weeks 11-12: Humanoid Robot Development
- Week 13: Conversational Robotics + Capstone

Bonus Features:
- Authentication (50 points): Better-Auth with user profiling
- Personalization (50 points): Per-chapter complexity adjustment
- Urdu Translation (50 points): Per-chapter translation with RTL support

Subagent Architecture (Orchestrator Pattern):
- Content Writer Subagent: Writes chapter markdown
- Embedding Generator Subagent: Processes text → embeddings
- Theme Stylist Subagent: CSS/styling decisions
- API Builder Subagent: FastAPI endpoint creation
- Chatbot Integrator Subagent: ChatKit + RAG wiring

Acceptance Criteria:
Base (100 points):
- Docusaurus book with all 4 modules + 13 weeks
- Purple/neon theme applied consistently
- OpenAI embeddings + Qdrant Cloud storage
- FastAPI backend with RAG endpoints
- Gemini via Context-7 MCP
- ChatKit embedded and functional
- Text selection RAG queries
- Deployed to GitHub Pages

Bonus (200 points):
- Better-Auth with profiling
- Per-chapter personalization
- Per-chapter Urdu translation
- Subagent skills documented

## Response snapshot

Constitution created successfully with version 1.0.0.

The constitution has been written to `.specify/memory/constitution.md` with the following structure:

1. **Core Mission**: AI-native interactive textbook for Physical AI & Humanoid Robotics
2. **7 Core Principles**:
   - I. User Experience First (purple/neon theme, responsive, accessible, performant)
   - II. Educational Excellence (progressive complexity, examples, visuals, assessments)
   - III. RAG-Only Answering (strict retrieval, no hallucination, citations required)
   - IV. Technical Stack Immutability (fixed hackathon tech requirements)
   - V. Code Quality Standards (TypeScript strict, Python type hints, testing, docs)
   - VI. Security Principles (API key protection, rate limiting, input validation, CORS)
   - VII. Performance Requirements (batch embeddings, RAG latency, build time, vector search)
3. **Content Architecture**: 4 modules across 13 weeks
4. **Bonus Feature Governance**: Authentication, Personalization, Urdu Translation
5. **Subagent Architecture**: Orchestrator pattern with 5 specialized subagents
6. **Acceptance Criteria**: Base requirements (100 pts) + Bonus (200 pts)
7. **Governance**: Amendment procedures and compliance enforcement

All placeholders have been filled with concrete values from the user input. No template tokens remain. The constitution includes a Sync Impact Report at the top documenting this as the initial v1.0.0 release.

Templates reviewed for alignment:
- ✅ plan-template.md: Constitution Check section compatible
- ✅ spec-template.md: Requirements structure aligns with principles
- ✅ tasks-template.md: Task organization supports all principles

## Outcome

- ✅ Impact: Project constitution established as authoritative governance document (v1.0.0)
- 🧪 Tests: N/A (documentation artifact)
- 📁 Files: Created/updated `.specify/memory/constitution.md` with complete governance framework
- 🔁 Next prompts: Use `/sp.specify` to create feature specs, `/sp.plan` for implementation planning, `/sp.tasks` for task breakdown
- 🧠 Reflection: Constitution provides clear technical constraints (fixed stack), quality gates (7 principles), and success criteria (base + bonus points). The RAG-Only Answering principle is marked CRITICAL and will require careful validation during implementation.

## Evaluation notes (flywheel)

- Failure modes observed: None. All placeholders filled successfully. Version semantics applied correctly (1.0.0 for initial).
- Graders run and results (PASS/FAIL): PASS - All validation checks passed (no unexplained brackets, dates in ISO format, principles declarative and testable)
- Prompt variant (if applicable): Standard constitution creation workflow
- Next experiment (smallest change to try): Consider adding explicit performance budgets for each principle (e.g., build time thresholds, test coverage percentages) in future amendments
