---
id: 0002
title: Constitution Gemini Embeddings Amendment
stage: constitution
date: 2025-11-29
surface: agent
model: claude-sonnet-4-5-20250929
feature: none
branch: 001-physical-ai-textbook
user: developer
command: /sp.constitution
labels: ["constitution", "embeddings", "gemini", "technical-stack"]
links:
  spec: null
  ticket: null
  adr: null
  pr: null
files:
  - .specify/memory/constitution.md
tests:
  - N/A (Constitution document, no automated tests)
---

## Prompt

update the setting for embeddings i will not be using open ai instead i will use gemini model gemini-embedding-001 for that also update it everywhere where u have used openai model update it to gemini model for embeddings

## Response snapshot

Updated constitution from v1.0.0 to v1.1.0 with the following changes:

**Principle IV: Technical Stack Immutability**
- Changed embeddings from `OpenAI API (text-embedding-3-small)` to `Gemini API (gemini-embedding-001)`

**Principle VII: Performance Requirements**
- Updated batch embedding reference from "OpenAI API calls" to "Gemini API calls"

**Subagent Architecture**
- Updated Embedding Generator Subagent description to reference Gemini embeddings

**Acceptance Criteria**
- Updated base requirement from "OpenAI embeddings" to "Gemini embeddings"

**Sync Impact Report**
- Documented all changes in HTML comment header
- Identified follow-up TODOs:
  - Update backend/embedding service to use Gemini API (google.generativeai library)
  - Update environment variable configuration (.env.example, deployment configs)
  - Update any documentation referencing OpenAI embeddings

**Amendment History**
- Added entry: "2025-11-29 | Embedding model change to Gemini (v1.1.0) | Switched from OpenAI text-embedding-3-small to Gemini gemini-embedding-001 per hackathon requirements"

## Outcome

- ✅ Impact: Constitution successfully amended to replace all OpenAI embedding references with Gemini gemini-embedding-001
- 🧪 Tests: No automated tests for constitution; manual validation performed
- 📁 Files: 1 file modified (.specify/memory/constitution.md)
- 🔁 Next prompts: Implement backend embedding service using Gemini API; update environment variables
- 🧠 Reflection: This is a MINOR version bump (1.0.0 → 1.1.0) because it materially changes a technical stack specification while maintaining backward compatibility in principle structure

## Evaluation notes (flywheel)

- Failure modes observed: None
- Graders run and results (PASS/FAIL): Manual review PASS - all OpenAI references replaced with Gemini
- Prompt variant (if applicable): N/A
- Next experiment (smallest change to try): Implement Gemini embedding generation in backend service
