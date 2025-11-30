---

description: "Task list for Physical AI & Humanoid Robotics Textbook implementation"
---

# Tasks: Physical AI & Humanoid Robotics Textbook

**Input**: Design documents from `/specs/001-physical-ai-textbook/`
**Prerequisites**: plan.md (required), spec.md (required for user stories), research.md, data-model.md, contracts/

**Tests**: Test tasks are included as requested by the feature specification.

**Organization**: Tasks are grouped by user story to enable independent implementation and testing of each story.

## Format: `[ID] [P?] [Story] Description`

- **[P]**: Can run in parallel (different files, no dependencies)
- **[Story]**: Which user story this task belongs to (e.g., US1, US2, US3)
- Include exact file paths in descriptions

## Path Conventions

- **Web app**: `backend/src/`, `frontend/src/`

## Phase 1: Setup (Project Initialization & Core Infrastructure)

**Purpose**: Project initialization and basic structure for both frontend and backend.

- [ ] T001 [P] Create `backend/` directory and initialize Python project in `backend/`
- [ ] T002 [P] Create `frontend/` directory and initialize Docusaurus project in `frontend/`
- [ ] T003 [P] Create `.env.example` for backend in `backend/.env.example`
- [ ] T004 [P] Create `.env.example` for frontend in `frontend/.env.example`
- [ ] T005 [P] Configure `requirements.txt` for backend in `backend/requirements.txt`
- [ ] T006 [P] Configure `package.json` for frontend in `frontend/package.json`
- [ ] T007 Create `src/main.py` for FastAPI app entry point in `backend/src/main.py`
- [ ] T008 Create base `docusaurus.config.js` in `frontend/docusaurus.config.js`
- [ ] T009 Create base `sidebars.js` in `frontend/sidebars.js`

---

## Phase 2: Foundational (Blocking Prerequisites)

**Purpose**: Core infrastructure that MUST be complete before ANY user story can be implemented.

**⚠️ CRITICAL**: No user story work can begin until this phase is complete

- [ ] T010 [P] Implement `config.py` for environment variables in `backend/src/config.py`
- [ ] T011 [P] Implement `cors.py` middleware in `backend/src/middleware/cors.py`
- [ ] T012 [P] Implement `rate_limit.py` middleware in `backend/src/middleware/rate_limit.py`
- [ ] T013 [P] Implement `error_handler.py` middleware in `backend/src/middleware/error_handler.py`
- [ ] T014 [P] Create `health.py` API route in `backend/src/api/health.py`
- [ ] T015 [P] Create `qdrant_client.py` service in `backend/src/services/qdrant_client.py`
- [ ] T016 [P] Create `embeddings.py` service for OpenAI embedding generation in `backend/src/services/embeddings.py`
- [ ] T017 Create `generate_embeddings.py` script for one-time embedding generation in `backend/scripts/generate_embeddings.py`
- [ ] T018 Integrate middlewares and health route into `backend/src/main.py`
- [ ] T019 Configure Docusaurus custom CSS for purple/neon theme in `frontend/src/css/custom.css`
- [ ] T020 Configure `tsconfig.json` for TypeScript strict mode in `frontend/tsconfig.json`

**Checkpoint**: Foundation ready - user story implementation can now begin in parallel

---

## Phase 3: User Story 1 - Read Structured Course Content (Priority: P1) 🎯 MVP

**Goal**: Enable students to read well-structured chapters with code examples, visual aids, and effective navigation.

**Independent Test**: Navigate to any module and verify: clear introduction present, learning objectives listed, code examples are syntax-highlighted and copyable, images/diagrams render correctly, sidebar navigation allows jumping between sections.

### Tests for User Story 1 (OPTIONAL - only if tests requested) ⚠️

> **NOTE: Write these tests FIRST, ensure they FAIL before implementation**

- [ ] T021 [P] [US1] Frontend unit test for sidebar navigation in `frontend/tests/unit/sidebar.test.tsx`
- [ ] T022 [P] [US1] Frontend integration test for content rendering and copy-to-clipboard in `frontend/tests/integration/content.test.tsx`

### Implementation for User Story 1

- [ ] T023 [US1] Create basic Docusaurus pages (`index.tsx`) in `frontend/src/pages/index.tsx`
- [ ] T024 [US1] Create example MDX content for Module 1, Week 1 in `frontend/docs/module-1-ros2/week-01-intro.mdx`
- [ ] T025 [P] [US1] Implement custom `CodeBlock` component with copy button in `frontend/src/components/CodeBlock.tsx`
- [ ] T026 [US1] Integrate `CodeBlock` into Docusaurus MDX rendering
- [ ] T027 [P] [US1] Ensure images and diagrams render correctly in MDX content
- [ ] T028 [US1] Configure Docusaurus sidebar to reflect module/week structure in `frontend/sidebars.js`
- [ ] T029 [US1] Populate all 4 main modules with introductory MDX files in `frontend/docs/`
- [ ] T030 [US1] Populate 13 weeks of structured content with example MDX files in `frontend/docs/`

**Checkpoint**: At this point, User Story 1 should be fully functional and testable independently

---

## Phase 4: User Story 2 - Ask Questions via Embedded Chatbot (Priority: P1)

**Goal**: Provide an embedded RAG chatbot that answers questions exclusively from book content with citations.

**Independent Test**: Open chatbot widget, ask "What is ROS 2?", verify response includes citation to specific chapter/section, verify response time is under 3 seconds. Ask question not covered in book and verify chatbot states information not found.

### Tests for User Story 2 ⚠️

- [ ] T031 [P] [US2] Backend unit test for `generate_embeddings_batch` in `backend/tests/unit/test_embeddings.py`
- [ ] T032 [P] [US2] Backend unit test for Qdrant client operations (collection, upsert, search) in `backend/tests/unit/test_qdrant_client.py`
- [ ] T033 [P] [US2] Backend unit test for `generate_rag_response` in `backend/tests/unit/test_gemini_chat.py`
- [ ] T034 [P] [US2] Backend integration test for `/api/chat` endpoint in `backend/tests/integration/test_chat_api.py`
- [ ] T035 [P] [US2] Frontend unit test for `ChatWidget` component in `frontend/tests/unit/ChatWidget.test.tsx`
- [ ] T036 [P] [US2] E2E test for chatbot interaction and citation display in `tests/e2e/test_chatbot.spec.ts`

### Implementation for User Story 2

- [ ] T037 [US2] Define Pydantic models for chat in `backend/src/models/chat.py`
- [ ] T038 [US2] Define Pydantic models for embeddings in `backend/src/models/embedding.py`
- [ ] T039 [US2] Implement `gemini_chat.py` service for RAG responses in `backend/src/services/gemini_chat.py`
- [ ] T040 [US2] Implement `/api/chat` endpoint in `backend/src/api/chat.py`
- [ ] T041 [US2] Implement `ChatWidget.tsx` component using ChatKit SDK in `frontend/src/components/ChatWidget.tsx`
- [ ] T042 [US2] Create `useChatAPI.ts` hook for frontend-backend communication in `frontend/src/hooks/useChatAPI.ts`
- [ ] T043 [US2] Integrate `ChatWidget` as a floating component in Docusaurus (via swizzling or plugin)
- [ ] T044 [US2] Run `backend/scripts/generate_embeddings.py` to populate Qdrant
- [ ] T045 [US2] Implement logic for "information not found" responses
- [ ] T046 [US2] Ensure chat message history persists within session

**Checkpoint**: At this point, User Stories 1 AND 2 should both work independently

---

## Phase 5: User Story 3 - Ask Questions About Selected Text (Priority: P2)

**Goal**: Enable learners to select text and ask hyper-focused questions about only that selection.

**Independent Test**: Select a paragraph about URDF, click "Ask about this" button, ask "Explain this in simpler terms", verify answer is scoped only to the selected text and includes disclaimer about context limitation.

### Tests for User Story 3 ⚠️

- [ ] T047 [P] [US3] Frontend unit test for `useTextSelection` hook in `frontend/tests/unit/useTextSelection.test.ts`
- [ ] T048 [P] [US3] Backend integration test for `/api/chat/selection` endpoint in `backend/tests/integration/test_chat_selection_api.py`
- [ ] T049 [P] [US3] E2E test for text selection and scoped chat response in `tests/e2e/test_text_selection_chat.spec.ts`

### Implementation for User Story 3

- [ ] T050 [US3] Implement `useTextSelection.ts` hook in `frontend/src/hooks/useTextSelection.ts`
- [ ] T051 [US3] Create `TextSelectionButton.tsx` component in `frontend/src/components/TextSelectionButton.tsx`
- [ ] T052 [US3] Integrate `TextSelectionButton` with content pages to appear on text selection
- [ ] T053 [US3] Implement `/api/chat/selection` endpoint in `backend/src/api/chat.py`
- [ ] T054 [US3] Modify `gemini_chat.py` to handle scoped context from selected text
- [ ] T055 [US3] Ensure chatbot response explicitly states it's based on selected text

**Checkpoint**: All user stories up to P2 should now be independently functional

---

## Phase 6: User Story 4 - Sign Up and Create Profile (Priority: P3 - Bonus)

**Goal**: Allow new users to sign up, provide background information, and persist their session.

**Independent Test**: Click "Sign Up" button, complete email/password form, answer profile questions (programming experience, hardware familiarity), submit and verify account creation. Sign out and sign in again to verify session persistence.

### Tests for User Story 4 ⚠️

- [ ] T056 [P] [US4] Backend unit test for `auth_service.py` (signup, signin, signout) in `backend/tests/unit/test_auth_service.py`
- [ ] T057 [P] [US4] Backend integration test for `/api/auth` endpoints in `backend/tests/integration/test_auth_api.py`
- [ ] T058 [P] [US4] Frontend unit test for signup/signin forms in `frontend/tests/unit/auth_forms.test.tsx`
- [ ] T059 [P] [US4] E2E test for user signup, signin, and session persistence in `tests/e2e/test_auth.spec.ts`

### Implementation for User Story 4

- [ ] T060 [US4] Define Pydantic model for user profile in `backend/src/models/user.py`
- [ ] T061 [US4] Implement initial `auth_service.py` for Better-Auth integration in `backend/src/services/auth_service.py`
- [ ] T062 [US4] Implement `/api/auth/signup`, `/api/auth/signin`, `/api/auth/signout` endpoints in `backend/src/api/auth.py`
- [ ] T063 [US4] Create `user_profiles` table in Neon Postgres (via `asyncpg` or migration script)
- [ ] T064 [US4] Create `signin.tsx` and `signup.tsx` pages in `frontend/src/pages/auth/`
- [ ] T065 [US4] Add navigation links for signup/signin in frontend
- [ ] T066 [US4] Implement session persistence via cookies on the frontend

**Checkpoint**: User Story 4 is functional and can be independently tested.

---

## Phase 7: User Story 5 - Personalize Chapter Content (Priority: P3 - Bonus)

**Goal**: Allow registered users to personalize chapter content to their specific learning level.

**Independent Test**: Sign in as user with "beginner" programming level, navigate to Week 5, click "Personalize" button, verify content adjusts to simpler explanations. Verify original content is still accessible via toggle.

### Tests for User Story 5 ⚠️

- [ ] T067 [P] [US5] Backend unit test for `personalization.py` service in `backend/tests/unit/test_personalization_service.py`
- [ ] T068 [P] [US5] Backend integration test for `/api/personalize` endpoint in `backend/tests/integration/test_personalization_api.py`
- [ ] T069 [P] [US5] Frontend unit test for `PersonalizeButton.tsx` and content toggle in `frontend/tests/unit/PersonalizeButton.test.tsx`
- [ ] T070 [P] [US5] E2E test for content personalization and toggle in `tests/e2e/test_personalization.spec.ts`

### Implementation for User Story 5

- [ ] T071 [US5] Implement `personalization.py` service to adapt content based on user profile in `backend/src/services/personalization.py`
- [ ] T072 [US5] Implement `/api/personalize` endpoint in `backend/src/api/personalization.py`
- [ ] T073 [US5] Create `PersonalizeButton.tsx` component in `frontend/src/components/PersonalizeButton.tsx`
- [ ] T074 [US5] Integrate `PersonalizeButton` into chapter pages
- [ ] T075 [US5] Implement frontend logic to display personalized content or original content via toggle
- [ ] T076 [US5] Cache personalized content for the session in backend

**Checkpoint**: User Story 5 is functional and can be independently tested.

---

## Phase 8: User Story 6 - Translate Chapter to Urdu (Priority: P3 - Bonus)

**Goal**: Enable learners to translate chapter content to Urdu with RTL layout and technical term preservation.

**Independent Test**: Navigate to Week 4, click "Translate to Urdu" button, verify content translates to Urdu with RTL layout applied, verify technical terms (ROS 2, URDF, Gazebo) remain in English.

### Tests for User Story 6 ⚠️

- [ ] T077 [P] [US6] Backend unit test for Urdu translation service in `backend/tests/unit/test_urdu_translation_service.py`
- [ ] T078 [P] [US6] Backend integration test for `/api/translate` endpoint in `backend/tests/integration/test_translation_api.py`
- [ ] T079 [P] [US6] Frontend unit test for `TranslateButton.tsx` and RTL styling in `frontend/tests/unit/TranslateButton.test.tsx`
- [ ] T080 [P] [US6] E2E test for Urdu translation and RTL layout in `tests/e2e/test_translation.spec.ts`

### Implementation for User Story 6

- [ ] T081 [US6] Implement Urdu translation service (using Gemini or other NLP service) in `backend/src/services/urdu_translation.py`
- [ ] T082 [US6] Implement `/api/translate` endpoint in `backend/src/api/translation.py`
- [ ] T083 [US6] Create `translation_cache` table in Neon Postgres (via `asyncpg` or migration script)
- [ ] T084 [US6] Create `TranslateButton.tsx` component in `frontend/src/components/TranslateButton.tsx`
- [ ] T085 [US6] Integrate `TranslateButton` into chapter pages
- [ ] T086 [US6] Implement frontend CSS for RTL layout in `frontend/src/css/custom.css`
- [ ] T087 [US6] Implement logic to preserve technical terms (ROS 2, URDF, etc.) in English within Urdu text
- [ ] T088 [US6] Implement translation caching mechanism in backend

**Checkpoint**: User Story 6 is functional and can be independently tested.

---

## Phase 9: Polish & Cross-Cutting Concerns

**Purpose**: General improvements that affect multiple user stories.

- [ ] T089 Update all relevant documentation files (READMEs, quickstart.md)
- [ ] T090 Review and refactor common code where applicable (e.g., utility functions)
- [ ] T091 Perform overall performance optimization (e.g., image optimization, frontend bundle size)
- [ ] T092 Add additional unit tests for any uncovered areas in `backend/tests/unit/` and `frontend/tests/unit/`
- [ ] T093 Conduct comprehensive security review for all API endpoints
- [ ] T094 Verify `quickstart.md` setup steps are accurate and complete
- [ ] T095 Implement CI/CD pipelines for frontend and backend deployment on GitHub Actions

---

## Dependencies & Execution Order

### Phase Dependencies

- **Setup (Phase 1)**: No dependencies - can start immediately
- **Foundational (Phase 2)**: Depends on Setup completion - BLOCKS all user stories
- **User Stories (Phase 3+)**: All depend on Foundational phase completion
  - User stories can then proceed in parallel (if staffed)
  - Or sequentially in priority order (P1 → P2 → P3)
- **Polish (Final Phase)**: Depends on all desired user stories being complete

### User Story Dependencies

- **User Story 1 (P1)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 2 (P1)**: Can start after Foundational (Phase 2) - Depends on US1 (content to embed)
- **User Story 3 (P2)**: Can start after Foundational (Phase 2) - Depends on US1 (content to select) and US2 (chatbot for selection query)
- **User Story 4 (P3)**: Can start after Foundational (Phase 2) - No dependencies on other stories
- **User Story 5 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (content to personalize) and US4 (user profile)
- **User Story 6 (P3)**: Can start after Foundational (Phase 2) - Depends on US1 (content to translate)

### Within Each User Story

- Tests (if included) MUST be written and FAIL before implementation
- Models before services
- Services before endpoints
- Core implementation before integration
- Story complete before moving to next priority

### Parallel Opportunities

- All Setup tasks marked [P] can run in parallel
- All Foundational tasks marked [P] can run in parallel (within Phase 2)
- Once Foundational phase completes, User Stories 1, 2 (after 1), 3 (after 1&2), 4, 5 (after 1&4), 6 (after 1) can proceed. US4 can run in parallel with US1, US2, US3.
- All tests for a user story marked [P] can run in parallel
- Different user stories can be worked on in parallel by different team members (e.g., US1 and US4 can start in parallel after Foundational)

---

## Parallel Example: User Story 1

```bash
# Launch all tests for User Story 1 together:
Task: "Frontend unit test for sidebar navigation in frontend/tests/unit/sidebar.test.tsx"
Task: "Frontend integration test for content rendering and copy-to-clipboard in frontend/tests/integration/content.test.tsx"

# Launch parallel implementation tasks for User Story 1:
Task: "Implement custom CodeBlock component with copy button in frontend/src/components/CodeBlock.tsx"
Task: "Ensure images and diagrams render correctly in MDX content"
```

---

## Implementation Strategy

### MVP First (User Story 1 & 2 only)

1. Complete Phase 1: Setup
2. Complete Phase 2: Foundational (CRITICAL - blocks all stories)
3. Complete Phase 3: User Story 1
4. Complete Phase 4: User Story 2
5. **STOP and VALIDATE**: Test User Stories 1 & 2 independently
6. Deploy/demo if ready

### Incremental Delivery

1. Complete Setup + Foundational → Foundation ready
2. Add User Story 1 → Test independently → Deploy/Demo (MVP!)
3. Add User Story 2 → Test independently → Deploy/Demo
4. Add User Story 3 → Test independently → Deploy/Demo
5. Add User Story 4 → Test independently → Deploy/Demo
6. Add User Story 5 → Test independently → Deploy/Demo
7. Add User Story 6 → Test independently → Deploy/Demo
8. Each story adds value without breaking previous stories

### Parallel Team Strategy

With multiple developers:

1. Team completes Setup + Foundational together
2. Once Foundational is done:
   - Developer A: User Story 1 (Content)
   - Developer B: User Story 4 (Auth - independent)
   - Developer C: User Story 2 (Chatbot - depends on US1 content)
   - Developer D: User Story 3 (Text Selection - depends on US1, US2)
3. Stories complete and integrate independently

---

## Notes

- [P] tasks = different files, no dependencies
- [Story] label maps task to specific user story for traceability
- Each user story should be independently completable and testable
- Verify tests fail before implementing
- Commit after each task or logical group
- Stop at any checkpoint to validate story independently
- Avoid: vague tasks, same file conflicts, cross-story dependencies that break independence
