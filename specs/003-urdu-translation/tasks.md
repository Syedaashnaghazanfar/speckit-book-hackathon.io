# Implementation Tasks: Urdu Translation

**Feature**: 003-urdu-translation
**Branch**: `003-urdu-translation`
**Created**: 2025-11-30
**Spec**: [spec.md](./spec.md)
**Plan**: [plan.md](./plan.md)

## Task Overview

**Total Tasks**: 15
**User Stories**: 3 (P1, P2, P3)
**MVP Scope**: User Story 1 only (Global Language Toggle)
**Incremental Delivery**: Each user story is independently testable

## Implementation Strategy

This feature implements Urdu translation in 3 independent increments:

1. **US1 (P1)**: Global language toggle - Core value, full-site translation, 50-point bonus
2. **US2 (P2)**: Context menu translation - Flexibility enhancement, bilingual learning
3. **US3 (P3)**: Technical term preservation - Quality improvement, educational accuracy

Each story can be implemented, tested, and deployed independently.

---

## Phase 1: Setup & Foundational

**Goal**: Prepare project structure and shared infrastructure

### Tasks

- [ ] T001 Verify .gitignore includes node_modules/, dist/, .env*, __pycache__/, *.pyc
- [ ] T002 [P] Create backend translation models in backend/src/models/translation.py
- [ ] T003 [P] Create backend translation service in backend/src/services/translation.py
- [ ] T004 Create backend translation endpoint in backend/src/api/translate.py
- [ ] T005 [P] Create frontend LanguageContext in frontend/my-website/src/context/LanguageContext.tsx
- [ ] T006 [P] Create useLanguage hook in frontend/my-website/src/hooks/useLanguage.ts

**Acceptance Criteria**:
- Backend has translation API endpoint at POST /api/translate
- Frontend has global LanguageContext for language state
- Gemini API integrated for translation
- All tasks use strict TypeScript and Python type hints

---

## Phase 2: User Story 1 - Global Urdu Language Toggle (P1)

**Story Goal**: Enable Urdu-speaking users to view entire website in their native language with RTL layout

**Why P1**: Core value proposition, addresses hackathon bonus (50 points), makes entire site accessible to Urdu speakers

**Independent Test**: Click Urdu toggle → verify all text displays in Urdu → verify RTL layout → verify purple/neon theme maintained → refresh browser → verify language persists

### Acceptance Scenarios (from spec.md)

1. Click Urdu button → all content translates + RTL applies
2. Navigate to new page → Urdu + RTL maintained
3. Click button again → switches back to English + LTR
4. Close/reopen browser → language preference remembered
5. Purple/neon theme identical in both languages

### Tasks

- [ ] T007 [US1] Create LanguageToggle component in frontend/my-website/src/components/LanguageToggle/index.tsx
- [ ] T008 [US1] Create LanguageToggle styles with purple/neon theme in frontend/my-website/src/components/LanguageToggle/LanguageToggle.module.css
- [ ] T009 [US1] Add LanguageToggle to navbar in frontend/my-website/docusaurus.config.ts (after "Course Modules" link)
- [ ] T010 [US1] Implement RTL CSS overrides in frontend/my-website/src/css/custom.css
- [ ] T011 [US1] Update ChatWidget for Urdu UI labels in frontend/my-website/src/components/ChatWidget/ChatWidget.tsx
- [ ] T012 [US1] Wrap app in LanguageProvider in frontend/my-website/src/theme/Root.tsx

**Validation Checklist** (before marking US1 complete):
- [ ] Language toggle button visible in navbar after "Course Modules"
- [ ] Clicking toggle translates all visible content to Urdu
- [ ] RTL layout applies (text-align: right, flexbox reversal)
- [ ] Purple/neon gradients maintained in both languages
- [ ] Language preference persists in localStorage
- [ ] Page navigation maintains language selection
- [ ] ChatWidget UI labels translate to Urdu
- [ ] All FR-001 through FR-006 verified

---

## Phase 3: User Story 2 - Context Menu Text Translation (P2)

**Story Goal**: Enable selective text translation via right-click for flexible bilingual learning

**Why P2**: Flexibility enhancement for users comfortable with English but needing occasional Urdu translations

**Independent Test**: Select text → right-click → click "Translate to Urdu" → verify inline Urdu translation → verify purple/neon theme on menu

### Acceptance Scenarios (from spec.md)

1. Select text → right-click → "Translate to Urdu" option appears with purple/neon styling
2. Click "Translate to Urdu" → selected text replaced with Urdu RTL inline
3. Translated text remains after deselection
4. Right-click Urdu text → "Translate to English" option appears
5. Global Urdu mode → context menu shows "Translate to English" instead

### Tasks

- [ ] T013 [US2] Create TranslationContextMenu component in frontend/my-website/src/components/TranslationContextMenu/index.tsx
- [ ] T014 [US2] Create TranslationContextMenu styles in frontend/my-website/src/components/TranslationContextMenu/TranslationContextMenu.module.css
- [ ] T015 [US2] Create useTranslation hook in frontend/my-website/src/hooks/useTranslation.ts
- [ ] T016 [US2] Integrate TranslationContextMenu with text selection in frontend/my-website/src/components/TextSelectionHandler/TextSelectionHandler.tsx

**Validation Checklist** (before marking US2 complete):
- [ ] Context menu appears on right-click of selected text
- [ ] Menu styled with purple/neon theme
- [ ] "Translate to Urdu" option visible in English mode
- [ ] Selected text replaced inline with Urdu translation
- [ ] Urdu text displays in RTL format
- [ ] "Translate to English" option visible when right-clicking Urdu text
- [ ] Global language switch updates context menu options
- [ ] All FR-007 through FR-009 verified

---

## Phase 4: User Story 3 - Technical Term Preservation (P3)

**Story Goal**: Intelligently preserve technical terms (ROS 2, SLAM, API) during translation for educational accuracy

**Why P3**: Quality enhancement, improves translation accuracy for technical content, can be refined iteratively

**Independent Test**: Translate page with "ROS 2", "SLAM", "neural network" → verify terms preserved in English → verify surrounding text in Urdu

### Acceptance Scenarios (from spec.md)

1. Content with acronyms (ROS 2, SLAM, API) → acronyms preserved, Urdu context around them
2. Programming terms (function, class, variable) → appropriately transliterated with meaning
3. Math symbols/code blocks → symbols unchanged, explanatory text in Urdu
4. Links/URLs → link text translates, URLs remain functional

### Tasks

- [ ] T017 [US3] Add technical term glossary to backend/src/services/translation.py
- [ ] T018 [US3] Update Gemini prompt with preserve_terms parameter in backend/src/services/translation.py
- [ ] T019 [US3] Add code block detection to skip translation in backend/src/services/translation.py

**Validation Checklist** (before marking US3 complete):
- [ ] Technical acronyms (ROS 2, SLAM, API) remain in English
- [ ] Code blocks remain unchanged (no translation)
- [ ] Mathematical symbols preserved
- [ ] URLs remain functional after translation
- [ ] Programming terms handled appropriately
- [ ] All FR-011 verified

---

## Phase 5: Polish & Cross-Cutting Concerns

**Goal**: Error handling, loading states, accessibility validation

### Tasks

- [ ] T020 [P] Add loading indicators during translation in LanguageToggle and TranslationContextMenu
- [ ] T021 [P] Add error handling for translation API failures in frontend/my-website/src/hooks/useTranslation.ts
- [ ] T022 Validate WCAG 2.1 AA compliance for all Urdu UI elements (keyboard nav, ARIA labels, screen reader)

**Validation Checklist**:
- [ ] Loading states visible during translation
- [ ] Error messages user-friendly if API fails
- [ ] Retry mechanism available on translation failure
- [ ] WCAG 2.1 AA compliance verified (axe-core, manual testing)
- [ ] Keyboard navigation works in both languages
- [ ] Screen reader announces language changes
- [ ] All SC-001 through SC-009 met

---

## Dependency Graph

```
Setup Phase (T001-T006)
    ↓
US1 (T007-T012) ← MVP scope (complete first)
    ↓
US2 (T013-T016) ← Independent of US3, depends on US1 infrastructure
    ↓
US3 (T017-T019) ← Independent of US2, enhances translation quality
    ↓
Polish (T020-T022) ← Applies to all user stories
```

**Parallel Opportunities**:
- T002, T003, T005, T006 can run in parallel (different files)
- T007, T008 can run in parallel (component + styles)
- T020, T021 can run in parallel (different concerns)

**Blocking Dependencies**:
- US1 must complete before US2 (context menu needs LanguageContext)
- US1 must complete before US3 (technical terms need translation service)
- T004 must complete before T007 (LanguageToggle needs backend API)

---

## Success Criteria Mapping

| Success Criterion | Tasks | Validation |
|-------------------|-------|------------|
| SC-001: <1s toggle | T007-T012 | Manual timing test |
| SC-002: 95% accuracy | T017-T019 | Manual translation review |
| SC-003: RTL browsers | T010 | Cross-browser testing |
| SC-004: Theme consistency | T008, T010, T014 | Visual comparison |
| SC-005: <3s context menu | T013-T016 | Manual timing test |
| SC-006: 100% persistence | T007, T012 | localStorage verification |
| SC-007: 90% satisfaction | All tasks | User testing with Urdu speakers |
| SC-008: WCAG AA | T022 | axe-core + manual testing |
| SC-009: Hackathon bonus | All tasks | Feature completeness check |

---

## Implementation Notes

**Tech Stack** (from existing codebase):
- Frontend: TypeScript 5.6.2, React 19, Docusaurus 3.9.2
- Backend: Python 3.11, FastAPI
- Translation: Gemini 1.5 Flash API
- Storage: Browser localStorage

**Critical Paths**:
1. Backend translation endpoint (T002-T004) → blocks all frontend work
2. LanguageContext (T005) → blocks all UI components
3. RTL CSS (T010) → critical for Urdu UX

**Performance Targets**:
- Language toggle: <1s (SC-001)
- Translation API: <3s (SC-005)
- Cache lookup: <500ms (plan.md)

**Quality Gates**:
- TypeScript strict mode enforced
- Python type hints required
- Purple/neon theme maintained
- WCAG 2.1 AA compliance

---

## Execution Order

**Recommended sequence** (respects dependencies, maximizes parallelism):

1. **Setup**: T001 → [T002, T003, T005, T006 parallel] → T004
2. **US1 (MVP)**: [T007, T008 parallel] → T009 → T010 → T011 → T012
3. **Validate US1**: Run US1 validation checklist, deploy if passing
4. **US2**: [T013, T014, T015 parallel] → T016
5. **Validate US2**: Run US2 validation checklist
6. **US3**: T017 → T018 → T019
7. **Validate US3**: Run US3 validation checklist
8. **Polish**: [T020, T021 parallel] → T022
9. **Final Validation**: Run all success criteria checks, deploy

**Incremental Delivery**:
- **Milestone 1** (MVP): Complete US1 → deploy → collect feedback → 50-point bonus achieved
- **Milestone 2**: Complete US2 → deploy → enhance flexibility
- **Milestone 3**: Complete US3 + Polish → deploy → maximize quality

---

## Task Completion Status

**Progress**: 0/22 tasks complete (0%)

**By Phase**:
- Setup: 0/6 complete
- US1 (P1): 0/6 complete
- US2 (P2): 0/4 complete
- US3 (P3): 0/3 complete
- Polish: 0/3 complete

**Next Task**: T001 (Verify .gitignore)
