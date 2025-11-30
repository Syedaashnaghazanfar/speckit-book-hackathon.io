---
id: 0003
title: Generate Implementation Tasks for Physical AI Textbook
stage: tasks
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: 001-physical-ai-textbook
branch: 001-physical-ai-textbook
user: default_user
command: /sp.tasks
labels: ["task-generation", "physical-ai-textbook"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - specs/001-physical-ai-textbook/tasks.md
tests:
null
---

## Prompt

```text
<command-message>sp.tasks is running…</command-message>
<command-name>/sp.tasks</command-name>
<command-args>Physical AI & Humanoid Robotics Textbook – Sub-Agent Driven Implementation Plan

Task ID: 001-physical-ai-textbook
Created: 2025-11-28
Execution Mode: STRICTLY VIA SUB-AGENTS + SKILLS if present otherwise u can do it youself too.

⚠️ IMPORTANT RULE (NON-NEGOTIABLE):
✅ Every phase MUST be executed using Claude/Gemini Sub-Agents if present
✅ Every repeated action MUST be turned into a Skill
✅ Sub-agents must be chosen wisely based on task nature
✅ Human role = Architect + Verifier ONLY PHASE 1: Foundation Setup
Task 1.1: Initialize Docusaurus Project

Priority: P0 (Critical)
Dependencies: None

Steps:

Create book/ directory

Run npx create-docusaurus@latest . classic --typescript

Clean up default content

Verify npm run start works

Acceptance Criteria:

Docusaurus dev server runs on port 3000

No TypeScript errors

Default theme loads

Task 1.2: Create Purple/Neon Theme [PARALLEL with 1.3]

Priority: P0 (Critical)
Dependencies: Task 1.1

Steps:

Create src/css/custom.css with CSS variables:

Primary: #8B5CF6 (Purple)

Secondary: #06B6D4 (Cyan/Neon)

Accent: #F472B6 (Pink)

Background: #0F0F23 (Dark)

Text: #E2E8F0

Apply neon glow effects to headers

Style code blocks with theme colors

Create gradient backgrounds

Acceptance Criteria:

All pages use purple/neon colors

Dark mode is default and only mode

Neon glow on headings and links

Consistent visual identity

Task 1.3: Initialize FastAPI Backend [PARALLEL with 1.2]

Priority: P0 (Critical)
Dependencies: None

Steps:

Create backend/ directory structure

Create requirements.txt with dependencies

Create app/main.py with basic FastAPI app

Set up CORS middleware

Create health check endpoint

Acceptance Criteria:

uvicorn app.main:app --reload works

/health returns {"status": "ok"}

CORS allows localhost origins

Task 1.4: Environment Configuration

Priority: P0 (Critical)
Dependencies: Task 1.1, Task 1.3

Steps:

Create .env.example with all required keys

Create backend/app/config.py using pydantic-settings

Add .env to .gitignore

Document environment setup in README

Acceptance Criteria:

Config loads from environment

Missing keys raise clear errors

Secrets not in git history

Task 1.5: Git Repository Setup

Priority: P1 (High)
Dependencies: Task 1.4

Steps:

Initialize git repository

Create comprehensive .gitignore

Create initial commit

Add GitHub Actions workflow for deployment (draft)

Acceptance Criteria:

Clean git history

No secrets committed

Actions workflow file exists

PHASE 2: Content Creation
Task 2.1: Book Introduction & Overview

Priority: P0 (Critical)
Dependencies: Task 1.1

Steps:

Create docs/intro.md with course overview

Add learning outcomes

Add course structure diagram

Add prerequisites section

Acceptance Criteria:

Introduction explains Physical AI concept

Clear module breakdown visible

Visually appealing with theme

Task 2.2: Module 1 - ROS 2 Content

Priority: P0 (Critical)
Dependencies: Task 2.1

Chapters:

module-1-ros2/01-introduction.md – What is ROS 2, history, why it matters

module-1-ros2/02-nodes-topics-services.md – Core concepts with code examples

module-1-ros2/03-rclpy-integration.md – Python integration for AI agents

module-1-ros2/04-urdf-humanoids.md – Robot description format

Acceptance Criteria:

Each chapter has learning objectives

Code examples are syntax highlighted

Diagrams explain architecture

Self-check questions at end

Task 2.3: Module 2 - Digital Twin Content

Priority: P0 (Critical)
Dependencies: Task 2.2

Chapters:

module-2-digital-twin/01-gazebo-intro.md – Simulation environment

module-2-digital-twin/02-physics-simulation.md – Gravity, collisions

module-2-digital-twin/03-unity-integration.md – High-fidelity rendering

module-2-digital-twin/04-sensor-simulation.md – LiDAR, cameras, IMU

Acceptance Criteria:

Gazebo setup instructions clear

Physics concepts explained visually

Sensor types compared in table

Task 2.4: Module 3 - NVIDIA Isaac Content

Priority: P0 (Critical)
Dependencies: Task 2.3

Chapters:

module-3-nvidia-isaac/01-isaac-sim.md – Photorealistic simulation

module-3-nvidia-isaac/02-isaac-ros.md – Hardware-accelerated VSLAM

module-3-nvidia-isaac/03-nav2-planning.md – Path planning for bipeds

module-3-nvidia-isaac/04-synthetic-data.md – Training data generation

Acceptance Criteria:

Isaac Sim setup documented

VSLAM concept explained

Nav2 integration shown

Task 2.5: Module 4 - VLA Content

Priority: P0 (Critical)
Dependencies: Task 2.4

Chapters:

module-4-vla/01-voice-to-action.md – OpenAI Whisper integration

module-4-vla/02-cognitive-planning.md – LLM to ROS 2 actions

module-4-vla/03-vision-language-models.md – VLM architecture

module-4-vla/04-capstone-project.md – Autonomous humanoid project

Acceptance Criteria:

Whisper pipeline explained

LLM→Action mapping clear

Capstone requirements detailed

Task 2.6: Hardware Requirements Section

Priority: P1 (High)
Dependencies: Task 2.5

Content:

Workstation requirements (RTX 4070+, 64GB RAM)

Edge computing kits (Jetson Orin)

Sensor packages (RealSense, IMU)

Robot options (Unitree Go2, G1)

Cost breakdown tables

Cloud alternatives

Acceptance Criteria:

Clear hardware specs with links

Budget options documented

Tables for easy comparison

Task 2.7: Sidebar Configuration

Priority: P1 (High)
Dependencies: Task 2.6

Steps:

Create _category_.json for each module folder

Configure sidebars.ts for proper navigation

Add module icons if possible

Acceptance Criteria:

Sidebar shows all 4 modules

Chapters ordered correctly

Collapsible module sections

PHASE 3: Embedding Pipeline
Task 3.1: Qdrant Cloud Setup

Priority: P0 (Critical)
Dependencies: None

Steps:

Create Qdrant Cloud account

Create cluster (Free tier)

Create collection: physical_ai_book

Configure vector size: 1536

Note cluster URL and API key

Acceptance Criteria:

Cluster accessible via REST

Collection created with correct schema

Credentials stored in .env

Task 3.2: Embedding Generation Script

Priority: P0 (Critical)
Dependencies: Task 3.1, Task 2.7

Steps:

Create backend/scripts/generate_embeddings.py

Parse all MDX files from book/docs/

Chunk text: 500 tokens, 100 overlap

Generate embeddings via OpenAI API

Upload to Qdrant with metadata

Script Requirements:

{
  "chapter": "module-1-ros2",
  "section": "nodes-topics-services",
  "chunk_index": 0,
  "source_file": "02-nodes-topics-services.md"
}


Acceptance Criteria:

Script runs without errors

All chapters processed

Embeddings visible in Qdrant dashboard

Task 3.3: Verify Embeddings

Priority: P1 (High)
Dependencies: Task 3.2

Steps:

Query Qdrant with test vector

Verify metadata is correct

Test semantic search accuracy

Document collection size

Acceptance Criteria:

Search returns relevant chunks

Metadata accessible in results

Storage within Free tier limits

PHASE 4: RAG Backend
Task 4.1: Qdrant Service Module

Priority: P0 (Critical)
Dependencies: Task 3.3

Steps:

Create backend/app/services/qdrant_service.py

Implement search_similar(query: str, top_k: int)

Handle embedding generation for query

Return formatted results with metadata

Acceptance Criteria:

Service returns top_k results

Results include chapter/section info

Error handling for connection issues

Task 4.2: Gemini Service via MCP

Priority: P0 (Critical)
Dependencies: Task 4.1

Steps:

Create backend/app/services/gemini_service.py

Connect to Context-7 MCP server

Create generate_response(query: str, context: list)

Implement RAG-only system prompt

Parse and format response

System Prompt:

You are a teaching assistant for the "Physical AI & Humanoid Robotics" textbook.
ONLY answer from the provided context. If not found, say so.
Always cite: "📖 Source: [Chapter] > [Section]"


Acceptance Criteria:

Gemini responds via MCP

Responses cite sources

No hallucinations outside context

Task 4.3: Chat Endpoint

Priority: P0 (Critical)
Dependencies: Task 4.2

Steps:

Create backend/app/routers/chat.py

Implement POST /api/chat endpoint

Orchestrate: query → embed → search → generate

Format response with citations

Request/Response:

class ChatRequest(BaseModel):
    message: str
    session_id: Optional[str]

class ChatResponse(BaseModel):
    response: str
    citations: List[Citation]
    session_id: str


Acceptance Criteria:

Endpoint accepts POST requests

Returns valid JSON response

Citations included in response

Task 4.4: Selection Chat Endpoint

Priority: P0 (Critical)
Dependencies: Task 4.3

Steps:

Add POST /api/chat/selection endpoint

Accept selected_text parameter

Limit context to selected text ONLY

Include context_limited: true in response

Acceptance Criteria:

Only uses selected text as context

Clearly indicates limited context

Works with text of any length

Task 4.5: CORS and Production Config

Priority: P1 (High)
Dependencies: Task 4.4

Steps:

Configure CORS for production URLs

Add rate limiting (optional)

Set up error logging

Create production config

Acceptance Criteria:

CORS allows frontend domain

Errors logged with context

Production settings documented

PHASE 5: ChatKit Integration
Task 5.1: Install and Configure ChatKit

Priority: P0 (Critical)
Dependencies: Task 4.5

Steps:

Install ChatKit SDK: npm install @chatkit/react

Review ChatKit documentation

Create wrapper component

Acceptance Criteria:

SDK installed without conflicts

Basic component renders

Task 5.2: Create Chat Widget Component

Priority: P0 (Critical)
Dependencies: Task 5.1

Steps:

Create src/components/ChatWidget.tsx

Implement floating button + expandable panel

Add message input and display

Connect to /api/chat endpoint

Handle loading and error states

Acceptance Criteria:

Widget visible on all pages

Can minimize/maximize

Messages display correctly

Task 5.3: Text Selection Integration

Priority: P0 (Critical)
Dependencies: Task 5.2

Steps:

Add global text selection listener

Show "Ask about this" button on selection

Pass selected text to /api/chat/selection

Display response in chat widget

Acceptance Criteria:

Selection triggers popup button

Button sends to selection endpoint

Response clearly from selection context

Task 5.4: Theme Chat Widget

Priority: P1 (High)
Dependencies: Task 5.3

Steps:

Apply purple/neon colors to widget

Add neon border/glow effects

Style message bubbles

Ensure accessibility (contrast)

Acceptance Criteria:

Widget matches book theme

Readable text contrast

Consistent with overall design

PHASE 6: Deployment
Task 6.1: GitHub Pages Deployment

Priority: P0 (Critical)
Dependencies: Phase 5 complete

Steps:

Configure docusaurus.config.ts for GitHub Pages

Create GitHub Actions workflow

Set baseUrl correctly

Deploy and verify

Acceptance Criteria:

Site accessible at GitHub Pages URL

All assets load correctly

Navigation works

Task 6.2: API Deployment

Priority: P0 (Critical)
Dependencies: Task 6.1

Steps:

Create Vercel/Railway account

Deploy FastAPI application

Configure environment variables

Update CORS for production URL

Acceptance Criteria:

API accessible at production URL

Environment variables set

Health check passes

Task 6.3: End-to-End Testing

Priority: P0 (Critical)
Dependencies: Task 6.2

Steps:

Test complete user flow

Verify chat works in production

Test text selection feature

Check mobile responsiveness

Fix any deployment issues

Acceptance Criteria:

Full flow works: read → ask → answer

No CORS errors

Works on mobile

PHASE 7: Bonus Features (If Time Permits)
Task 7.1: Neon Postgres Setup

Priority: P2 (Bonus)
Dependencies: None

Steps:

Create Neon account

Create database

Create users table

Note connection string

Task 7.2: Better-Auth Integration

Priority: P2 (Bonus)
Dependencies: Task 7.1

Steps:

Install better-auth

Configure with Neon adapter

Create signup/signin pages

Add auth state management

Task 7.3: Profile Signup Form

Priority: P2 (Bonus)
Dependencies: Task 7.2

Steps:

Create multi-step signup form

Ask: programming experience, hardware familiarity

Store profile in database

Task 7.4: Personalization Button

Priority: P2 (Bonus)
Dependencies: Task 7.3

Steps:

Create PersonalizeButton.tsx

Fetch user profile

Send content + profile to Gemini

Display personalized version

Task 7.5: Urdu Translation

Priority: P2 (Bonus)
Dependencies: Task 4.2

Steps:

Create TranslateButton.tsx

Send content to Gemini for translation

Apply RTL CSS

Display translated content

Task 7.6: RTL Styling

Priority: P2 (Bonus)
Dependencies: Task 7.5

Steps:

Add RTL CSS classes

Handle mixed LTR/RTL content

Test layout

The tasks.md should be immediately executable - each task must be specific enough that an LLM can complete it without additional context.

## Task Generation Rules

**CRITICAL**: Tasks MUST be organized by user story to enable independent implementation and testing.

**Tests are OPTIONAL**: Only generate test tasks if explicitly requested in the feature specification or if user requests TDD approach.

### Checklist Format (REQUIRED)

Every task MUST strictly follow this format:

```text
- [ ] [TaskID] [P?] [Story?] Description with file path
```

**Format Components**:

1. **Checkbox**: ALWAYS start with `- [ ]` (markdown checkbox)
2. **Task ID**: Sequential number (T001, T002, T003...) in execution order
3. **[P] marker**: Include ONLY if task is parallelizable (different files, no dependencies on incomplete tasks)
4. **[Story] label**: REQUIRED for user story phase tasks only
   - Format: [US1], [US2], [US3], etc. (maps to user stories from spec.md)
   - Setup phase: NO story label
   - Foundational phase: NO story label
   - User Story phases: MUST have story label
   - Polish phase: NO story label
5. **Description**: Clear action with exact file path

**Examples**:

- ✅ CORRECT: `- [ ] T001 Create project structure per implementation plan`
- ✅ CORRECT: `- [ ] T005 [P] Implement authentication middleware in src/middleware/auth.py`
- ✅ CORRECT: `- [ ] T012 [P] [US1] Create User model in src/models/user.py`
- ✅ CORRECT: `- [ ] T014 [US1] Implement UserService in src/services/user_service.py`
- ❌ WRONG: `- [ ] Create User model` (missing ID and Story label)
- ❌ WRONG: `T001 [US1] Create model` (missing checkbox)
- ❌ WRONG: `- [ ] [US1] Create User model` (missing Task ID)
- ❌ WRONG: `- [ ] T001 [US1] Create model` (missing file path)

### Task Organization

1. **From User Stories (spec.md)** - PRIMARY ORGANIZATION:
   - Each user story (P1, P2, P3...) gets its own phase
   - Map all related components to their story:
     - Models needed for that story
     - Services needed for that story
     - Endpoints/UI needed for that story
     - If tests requested: Tests specific to that story
   - Mark story dependencies (most stories should be independent)

2. **From Contracts**:
   - Map each contract/endpoint → to the user story it serves
   - If tests requested: Each contract → contract test task [P] before implementation in that story's phase

3. **From Data Model**:
   - Map each entity to the user story(ies) that need it
   - If entity serves multiple stories: Put in earliest story or Setup phase
   - Relationships → service layer tasks in appropriate story phase

4. **From Setup/Infrastructure**:
   - Shared infrastructure → Setup phase (Phase 1)
   - Foundational/blocking tasks → Foundational phase (Phase 2)
   - Story-specific setup → within that story's phase

### Phase Structure

- **Phase 1**: Setup (project initialization)
- **Phase 2**: Foundational (blocking prerequisites - MUST complete before user stories)
- **Phase 3+**: User Stories in priority order (P1, P2, P3...)
  - Within each story: Tests (if requested) → Models → Services → Endpoints → Integration
  - Each phase should be a complete, independently testable increment
- **Final Phase**: Polish & Cross-Cutting Concerns

---

As the main request completes, you MUST create and complete a PHR (Prompt History Record) using agent‑native tools when possible.

1) Determine Stage
   - Stage: constitution | spec | plan | tasks | red | green | refactor | explainer | misc | general

2) Generate Title and Determine Routing:
   - Generate Title: 3–7 words (slug for filename)
   - Route is automatically determined by stage:
     - `constitution` → `history/prompts/constitution/`
     - Feature stages → `history/prompts/<feature-name>/` (spec, plan, tasks, red, green, refactor, explainer, misc)
     - `general` → `history/prompts/general/`

3) Create and Fill PHR (Shell first; fallback agent‑native)
   - Run: `.specify/scripts/bash/create-phr.sh --title "<title>" --stage <stage> [--feature <name>] --json`
   - Open the file and fill remaining placeholders (YAML + body), embedding full PROMPT_TEXT (verbatim) and concise RESPONSE_TEXT.
   - If the script fails:
     - Read `.specify/templates/phr-template.prompt.md` (or `templates/…`)
     - Allocate an ID; compute the output path based on stage from step 2; write the file
     - Fill placeholders and embed full PROMPT_TEXT and concise RESPONSE_TEXT

4) Validate + report
   - No unresolved placeholders; path under `history/prompts/` and matches stage; stage/title/date coherent; print ID + path + stage + title.
   - On failure: warn, don't block. Skip only for `/sp.phr`.
```

## Response snapshot

```text
The `tasks.md` file has been generated successfully at `D:/code/Q4/hackhathon/hackhathon-book/specs/001-physical-ai-textbook/tasks.md`.

Here is a summary of the generated tasks:

**Total Task Count**: 95

**Task Count Per User Story**:
-   **Phase 1: Setup**: 9
-   **Phase 2: Foundational**: 11
-   **User Story 1 (P1)**: 10
-   **User Story 2 (P1)**: 10
-   **User Story 3 (P2)**: 9
-   **User Story 4 (P3 - Bonus)**: 11
-   **User Story 5 (P3 - Bonus)**: 10
-   **User Story 6 (P3 - Bonus)**: 12
-   **Phase 9: Polish & Cross-Cutting Concerns**: 7

**Parallel Opportunities Identified**:
-   Setup (Phase 1): 6 tasks ([P])
-   Foundational (Phase 2): 7 tasks ([P])
-   User Story 1: 2 test tasks ([P]), 2 implementation tasks ([P])
-   User Story 2: 6 test tasks ([P])
-   User Story 3: 3 test tasks ([P])
-   User Story 4: 4 test tasks ([P])
-   User Story 5: 4 test tasks ([P])
-   User Story 6: 4 test tasks ([P])
-   Parallel execution of independent user stories (e.g., US1 and US4 can start in parallel after Foundational phase).

**Independent Test Criteria for Each Story**:
-   **User Story 1**: "Navigate to any module and verify: clear introduction present, learning objectives listed, code examples are syntax-highlighted and copyable, images/diagrams render correctly, sidebar navigation allows jumping between sections."
-   **User Story 2**: "Open chatbot widget, ask "What is ROS 2?", verify response includes citation to specific chapter/section, verify response time is under 3 seconds. Ask question not covered in book and verify chatbot states information not found."
-   **User Story 3**: "Select a paragraph about URDF, click "Ask about this" button, ask "Explain this in simpler terms", verify answer is scoped only to the selected text and includes disclaimer about context limitation."
-   **User Story 4**: "Click "Sign Up" button, complete email/password form, answer profile questions (programming experience, hardware familiarity), submit and verify account creation. Sign out and sign in again to verify session persistence."
-   **User Story 5**: "Sign in as user with "beginner" programming level, navigate to Week 5, click "Personalize" button, verify content adjusts to simpler explanations. Verify original content is still accessible via toggle."
-   **User Story 6**: "Navigate to Week 4, click "Translate to Urdu" button, verify content translates to Urdu with RTL layout applied, verify technical terms (ROS 2, URDF, Gazebo) remain in English."

**Suggested MVP Scope**: User Story 1 (Read Structured Course Content) and User Story 2 (Ask Questions via Embedded Chatbot).

**Format Validation**: All 95 tasks strictly follow the checklist format: `- [ ] TXXX [P?] [Story?] Description with file path`.

The tasks are now ready for implementation.
```

## Outcome

- ✅ Impact: Generated `tasks.md` according to the provided implementation plan, breaking down the project into actionable steps for each user story and phase.
- 🧪 Tests: No tests were executed, but test tasks were generated as part of the plan.
- 📁 Files: `specs/001-physical-ai-textbook/tasks.md` was created.
- 🔁 Next prompts: Continue with the implementation by executing the tasks in `tasks.md`.
- 🧠 Reflection: The task generation process successfully translated a high-level plan into a detailed, executable checklist, incorporating dependencies and parallelization opportunities.

## Evaluation notes (flywheel)

- Failure modes observed: None during PHR creation. Previous `grep` commands failed, necessitating manual parsing and PHR creation.
- Graders run and results (PASS/FAIL): Not applicable.
- Prompt variant (if applicable): Not applicable.
- Next experiment (smallest change to try): Automate PHR generation and validation to avoid manual steps.
