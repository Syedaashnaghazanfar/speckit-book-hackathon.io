# Feature Specification: Urdu Translation

**Feature Branch**: `003-urdu-translation`
**Created**: 2025-11-30
**Status**: Draft
**Input**: User description: "lets implement urdu translation feature we will add a button in the navbar after course modules and when that button will be clicked the full website converts to urdu or if user wants specific text that is selected to be in urdu then the user will select the text and right click there will an option translate to urdu and the text gets translated to urdu ensure our theme is maintained"

## User Scenarios & Testing *(mandatory)*

### User Story 1 - Global Urdu Language Toggle (Priority: P1)

Urdu-speaking users need to view the entire website in their native language for better comprehension and learning experience, requiring a prominent language toggle in the navigation that converts all content to Urdu while maintaining the site's visual design.

**Why this priority**: This is the core value proposition - enabling Urdu-speaking students to access Physical AI education in their native language. Without global translation, the feature provides minimal value. This directly addresses the hackathon bonus requirement for full Urdu translation (50 points).

**Independent Test**: Can be fully tested by clicking the Urdu toggle button in navbar and verifying all visible text (navigation, headings, paragraphs, buttons) displays in Urdu with proper RTL layout. Delivers immediate value by making the entire site accessible to Urdu speakers.

**Acceptance Scenarios**:

1. **Given** a user is viewing the site in English, **When** they click the Urdu language button in the navbar, **Then** all page content translates to Urdu and text direction switches to right-to-left (RTL)
2. **Given** the site is displaying in Urdu, **When** the user navigates to a different page, **Then** the new page loads in Urdu with RTL layout maintained
3. **Given** the site is in Urdu mode, **When** the user clicks the language button again, **Then** all content switches back to English with left-to-right (LTR) layout
4. **Given** the user has selected Urdu, **When** they close and reopen the browser, **Then** the site remembers their language preference and displays in Urdu
5. **Given** the site is in Urdu mode, **When** viewing any page, **Then** the purple/neon theme colors and styling remain exactly as they appear in English mode

---

### User Story 2 - Context Menu Text Translation (Priority: P2)

Users who prefer English but occasionally need Urdu translations for specific concepts can select any text on the page and translate just that selection via a right-click context menu, enabling flexible bilingual learning.

**Why this priority**: This provides flexibility for users who are comfortable with English but want to clarify specific technical terms or concepts in Urdu. It's a valuable supplement to the global toggle but not essential for the core translation feature. Supports mixed-language learning workflows.

**Independent Test**: Can be fully tested by selecting any paragraph, right-clicking to open context menu, selecting "Translate to Urdu" option, and verifying the selected text is replaced with Urdu translation in RTL format inline. Delivers value by enabling on-demand translation without changing entire page.

**Acceptance Scenarios**:

1. **Given** a user selects text on any page, **When** they right-click the selection, **Then** a context menu appears with "Translate to Urdu" option styled with the purple/neon theme
2. **Given** a user right-clicks selected text and chooses "Translate to Urdu", **When** the translation completes, **Then** the selected text is replaced inline with its Urdu translation in RTL format
3. **Given** text has been translated to Urdu via context menu, **When** the user clicks elsewhere or deselects, **Then** the Urdu translation remains visible in the page
4. **Given** translated text is displayed, **When** the user right-clicks the Urdu text, **Then** a context menu appears with "Translate to English" option to reverse the translation
5. **Given** the global language is set to Urdu, **When** the user selects text and right-clicks, **Then** the context menu shows "Translate to English" instead of "Translate to Urdu"

---

### User Story 3 - Urdu Translation of Technical Terms (Priority: P3)

Technical robotics and AI terminology should be intelligently handled during translation, either preserving English terms when standard practice or providing Urdu transliterations that maintain meaning, ensuring educational content remains accurate and understandable.

**Why this priority**: While important for quality, this is an enhancement to the translation accuracy rather than core functionality. P1 and P2 already enable translation; this improves the quality of translations for technical content. Can be refined iteratively after basic translation works.

**Independent Test**: Can be fully tested by translating pages with technical terms (e.g., "ROS 2", "SLAM", "neural network") and verifying they are handled appropriately (either preserved in English with Urdu context or properly transliterated). Delivers value by maintaining educational accuracy in translations.

**Acceptance Scenarios**:

1. **Given** content contains technical acronyms (ROS 2, SLAM, API), **When** translated to Urdu, **Then** acronyms are preserved in English but surrounded by Urdu explanatory text
2. **Given** content contains programming terms (function, class, variable), **When** translated to Urdu, **Then** terms are transliterated appropriately with context that maintains meaning
3. **Given** content contains mathematical symbols or code blocks, **When** translated to Urdu, **Then** symbols and code remain unchanged while surrounding explanatory text translates to Urdu
4. **Given** content contains links and URLs, **When** translated to Urdu, **Then** link text translates but URLs remain functional and unchanged

---

### Edge Cases

- What happens when translation service is unavailable or times out? (Show error message, allow retry, keep original text)
- How does the system handle mixed English/Urdu content after selective translation? (Maintain both languages inline with proper directionality)
- What happens when user switches global language while viewing a page with selectively translated text? (Clear selective translations, apply global language consistently)
- How are navigation menus, buttons, and UI elements handled in RTL mode? (Reverse layout, flip icons where appropriate)
- What happens to embedded media (images, videos) with English captions? (Translate captions if text-based, preserve media)
- How are code snippets and technical diagrams handled? (Preserve code as-is, translate comments and labels)
- What happens when user translates the same text multiple times? (Replace previous translation with new one)
- How does the chatbot handle Urdu mode? (ChatWidget should also translate its UI and potentially respond in Urdu)

## Requirements *(mandatory)*

### Functional Requirements

- **FR-001**: System MUST display a language toggle button in the navbar immediately after the "Course Modules" link
- **FR-002**: Language toggle button MUST be clearly labeled with both English ("اردو Urdu") and Urdu ("English انگریزی") depending on current language
- **FR-003**: System MUST translate all visible page content (headings, paragraphs, navigation, buttons, labels) when Urdu mode is activated
- **FR-004**: System MUST apply RTL (right-to-left) text direction to all translated Urdu content
- **FR-005**: System MUST persist language preference across page navigations and browser sessions
- **FR-006**: System MUST maintain the purple/neon gradient theme colors and styling identically in both English and Urdu modes
- **FR-007**: System MUST display "Translate to Urdu" option in right-click context menu when text is selected in English mode
- **FR-008**: System MUST display "Translate to English" option in right-click context menu when text is selected in Urdu mode
- **FR-009**: System MUST replace selected text inline with its translation when context menu translation is triggered
- **FR-010**: System MUST handle translation failures gracefully with user-friendly error messages and option to retry
- **FR-011**: System MUST preserve technical terminology appropriately (acronyms, code, URLs, mathematical symbols)
- **FR-012**: System MUST translate ChatWidget UI elements and messages when in Urdu mode
- **FR-013**: System MUST support reversible translations (English ↔ Urdu bidirectionally)
- **FR-014**: System MUST handle loading states during translation with visual indicators
- **FR-015**: System MUST maintain accessibility standards (screen reader support, keyboard navigation) in both languages

### Key Entities

- **Language Preference**: User's selected language (English or Urdu), persisted in browser storage, determines global site language
- **Translation Cache**: Mapping of English text to Urdu translations, stored to avoid redundant translation API calls
- **Context Menu State**: Tracks selected text, current language, and available translation actions
- **RTL Layout Config**: Configuration for text direction, layout mirroring, and icon flipping in Urdu mode

## Success Criteria *(mandatory)*

### Measurable Outcomes

- **SC-001**: Users can toggle between English and Urdu within 1 second, with all visible content translating successfully
- **SC-002**: 95% of page content translates accurately to Urdu while preserving technical accuracy
- **SC-003**: RTL layout displays correctly on all major browsers (Chrome, Firefox, Safari, Edge) without visual glitches
- **SC-004**: Purple/neon theme maintains visual consistency with zero color or styling changes between English and Urdu modes
- **SC-005**: Context menu translation completes for selections up to 500 words within 3 seconds
- **SC-006**: Language preference persists across 100% of page navigations and browser sessions
- **SC-007**: Translation feature achieves 90% user satisfaction in usability testing with Urdu speakers
- **SC-008**: Zero accessibility violations (WCAG AA compliance) in both English and Urdu modes
- **SC-009**: Feature meets hackathon bonus requirement criteria (50 points) for Urdu translation

## Assumptions

1. Users have internet connectivity for translation API calls (assume cloud-based translation service)
2. Urdu-speaking users are familiar with both Urdu script and basic English technical terminology
3. Primary users are students and educators in Pakistan, India, and Middle East where Urdu is spoken
4. Translation quality is acceptable for educational content (not legal/medical precision)
5. Users access the site primarily via desktop browsers with good RTL support
6. ChatWidget should translate but chatbot responses may remain in English (backend AI model limitation)
7. Embedded code blocks should not be translated (code is universal)
8. Images with English text will not have text extraction/translation (image translation is out of scope)
9. Translation service has reasonable rate limits and latency (<3 seconds per request)

## Dependencies

- Translation API service (e.g., Google Translate API, Microsoft Translator, or custom translation model)
- Browser storage API for persisting language preference
- Existing purple/neon theme CSS that must be verified for RTL compatibility
- ChatWidget component must be enhanced to support language switching

## Out of Scope

- Automatic language detection based on user's browser locale (manual toggle only)
- Translation of embedded images, videos, or non-text content
- Support for additional languages beyond English and Urdu
- Voice/speech synthesis in Urdu
- Real-time collaborative translation or crowdsourced improvements
- Offline translation capability (requires internet connection)
- Translation of user-generated content (only pre-existing textbook content)
- Backend AI chatbot responding in Urdu (chatbot UI translates, but responses remain English)
