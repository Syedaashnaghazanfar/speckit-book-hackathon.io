# Data Model: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-11-28
**Phase**: 1 (Design & Contracts)
**Status**: Complete

## Overview

This document defines the data entities, schemas, relationships, and validation rules for the Physical AI & Humanoid Robotics Textbook application.

---

## Entity Categories

1. **Content Entities**: Static textbook structure (modules, weeks, chapters)
2. **Vector Entities**: Embeddings stored in Qdrant
3. **Ephemeral Entities**: Runtime-only data (chat sessions, not persisted)
4. **Persistent Entities (Bonus)**: User profiles, translation cache (Neon Postgres)

---

## Content Entities

### 1. Module

**Purpose**: Top-level content organization (4 modules total)

**Schema**:
```python
class Module(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str  # e.g., "The Robotic Nervous System (ROS 2)"
    description: str
    learning_outcomes: List[str]
    order: int  # 1-4
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `title`: Max 100 characters
- `order`: Unique, range 1-4
- `learning_outcomes`: Min 3, max 5 outcomes

**Relationships**:
- One Module has many Weeks (1:N)

**Example**:
```json
{
  "id": "uuid-here",
  "title": "The Robotic Nervous System (ROS 2)",
  "description": "Learn the fundamentals of ROS 2...",
  "learning_outcomes": [
    "Understand ROS 2 architecture",
    "Create publisher-subscriber nodes",
    "Implement services and actions"
  ],
  "order": 1
}
```

---

### 2. Week

**Purpose**: Weekly content units (13 weeks total)

**Schema**:
```python
class Week(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    week_number: int  # 1-13
    title: str
    module_id: UUID  # FK to Module
    content_path: str  # Relative path to MDX file
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `week_number`: Unique, range 1-13
- `content_path`: Must match pattern `docs/module-*/week-*.mdx`
- `module_id`: Must exist in Module table

**Relationships**:
- One Week belongs to one Module (N:1)
- One Week has many Chapters (1:N)

**Example**:
```json
{
  "id": "uuid-here",
  "week_number": 3,
  "title": "ROS 2 Nodes and Topics",
  "module_id": "module-1-uuid",
  "content_path": "docs/module-1-ros2/week-03-nodes.mdx"
}
```

---

### 3. Chapter/Section

**Purpose**: Individual learning units within a week

**Schema**:
```python
class Chapter(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    title: str
    week_id: UUID  # FK to Week
    content: str  # Full MDX content
    position: int  # Order within week
    has_code_examples: bool = False
    has_assessments: bool = False
    created_at: datetime = Field(default_factory=datetime.utcnow)
    updated_at: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `title`: Max 150 characters
- `content`: Max 50,000 characters
- `position`: Unique within week

**Relationships**:
- One Chapter belongs to one Week (N:1)
- One Chapter has many EmbeddingChunks (1:N)

**Example**:
```json
{
  "id": "uuid-here",
  "title": "Understanding Pub/Sub Pattern",
  "week_id": "week-3-uuid",
  "content": "# Understanding Pub/Sub Pattern\n\nIn ROS 2...",
  "position": 1,
  "has_code_examples": true,
  "has_assessments": false
}
```

---

## Vector Entities

### 4. EmbeddingChunk

**Purpose**: Vector embeddings for RAG (stored in Qdrant Cloud)

**Schema** (Qdrant payload structure):
```python
class EmbeddingChunk(BaseModel):
    id: UUID = Field(default_factory=uuid4)
    chapter_id: UUID  # Reference to Chapter
    content: str  # Original text (500 tokens)
    embedding: List[float]  # 1536 dimensions (OpenAI text-embedding-3-small)
    metadata: EmbeddingMetadata
```

**Metadata Schema**:
```python
class EmbeddingMetadata(BaseModel):
    module: str  # e.g., "Module 1: ROS 2"
    week: int  # 1-13
    section: str  # e.g., "Nodes and Topics"
    page: int  # Position in chapter
    chunk_id: int  # Sequential chunk number
```

**Validation Rules**:
- `content`: Max 8,191 tokens (OpenAI limit)
- `embedding`: Exactly 1536 dimensions
- `metadata.week`: Range 1-13

**Qdrant Collection Config**:
```python
from qdrant_client.models import Distance, VectorParams

collection_config = VectorParams(
    size=1536,
    distance=Distance.COSINE  # Cosine similarity for semantic search
)
```

**Example**:
```json
{
  "id": "uuid-here",
  "chapter_id": "chapter-uuid",
  "content": "ROS 2 uses a Data Distribution Service (DDS) for communication...",
  "embedding": [0.023, -0.451, 0.892, ...],  # 1536 floats
  "metadata": {
    "module": "Module 1: ROS 2",
    "week": 3,
    "section": "DDS Architecture",
    "page": 2,
    "chunk_id": 5
  }
}
```

---

## Ephemeral Entities (Runtime Only)

### 5. ChatSession

**Purpose**: Temporary session for chat history (not persisted to database)

**Schema**:
```python
class ChatSession(BaseModel):
    session_id: UUID = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None  # Null for anonymous users
    messages: List[ChatMessage] = []
    created_at: datetime = Field(default_factory=datetime.utcnow)
```

**Storage**: In-memory cache (Redis or in-process dictionary)

**TTL**: 24 hours (session expires after inactivity)

**Example**:
```json
{
  "session_id": "uuid-here",
  "user_id": null,
  "messages": [
    {"role": "user", "content": "What is ROS 2?", "timestamp": "2025-11-28T10:00:00Z"},
    {"role": "assistant", "content": "ROS 2 is...", "citations": [...], "timestamp": "2025-11-28T10:00:02Z"}
  ],
  "created_at": "2025-11-28T10:00:00Z"
}
```

---

### 6. ChatMessage

**Purpose**: Individual message in a chat session

**Schema**:
```python
class ChatMessage(BaseModel):
    role: Literal["user", "assistant"]
    content: str
    citations: Optional[List[Citation]] = None  # Only for assistant messages
    timestamp: datetime = Field(default_factory=datetime.utcnow)
```

**Validation Rules**:
- `content`: Max 2,000 characters for user messages, max 1,000 for assistant
- `citations`: Required for assistant messages, null for user messages

**Example**:
```json
{
  "role": "assistant",
  "content": "ROS 2 is a robotics middleware framework...",
  "citations": [
    {"chapter": "Module 1: ROS 2", "section": "Introduction", "module": "ROS 2 Overview", "relevance": 0.95}
  ],
  "timestamp": "2025-11-28T10:00:02Z"
}
```

---

### 7. Citation

**Purpose**: Source attribution for assistant responses

**Schema**:
```python
class Citation(BaseModel):
    chapter: str  # e.g., "Module 1: ROS 2"
    section: str  # e.g., "Nodes and Topics"
    module: str  # e.g., "ROS 2 Overview"
    relevance: float  # 0.0-1.0 (Qdrant similarity score)
```

**Validation Rules**:
- `relevance`: Range 0.0-1.0

**Example**:
```json
{
  "chapter": "Module 1: ROS 2",
  "section": "Pub/Sub Pattern",
  "module": "ROS 2 Fundamentals",
  "relevance": 0.92
}
```

---

## Persistent Entities (Bonus Features)

### 8. UserProfile

**Purpose**: Authenticated user data (stored in Neon Postgres)

**Schema** (SQL):
```sql
CREATE TABLE user_profiles (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    email VARCHAR(255) UNIQUE NOT NULL,
    password_hash VARCHAR(255) NOT NULL,
    programming_experience VARCHAR(20) CHECK (programming_experience IN ('beginner', 'intermediate', 'advanced')),
    hardware_familiarity VARCHAR(20) CHECK (hardware_familiarity IN ('none', 'some', 'extensive')),
    preferred_language VARCHAR(2) DEFAULT 'en' CHECK (preferred_language IN ('en', 'ur')),
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP
);

CREATE INDEX idx_user_email ON user_profiles(email);
CREATE INDEX idx_last_login ON user_profiles(last_login);
```

**Pydantic Model** (Python):
```python
class UserProfile(BaseModel):
    id: UUID
    email: EmailStr
    password_hash: str
    programming_experience: Literal["beginner", "intermediate", "advanced"]
    hardware_familiarity: Literal["none", "some", "extensive"]
    preferred_language: Literal["en", "ur"] = "en"
    created_at: datetime
    last_login: Optional[datetime] = None
```

**Validation Rules**:
- `email`: Valid email format, unique
- `password_hash`: bcrypt hash (60 characters)

**Example**:
```json
{
  "id": "uuid-here",
  "email": "student@example.com",
  "programming_experience": "intermediate",
  "hardware_familiarity": "some",
  "preferred_language": "en",
  "created_at": "2025-11-28T10:00:00Z"
}
```

---

### 9. PersonalizationRequest

**Purpose**: Cached personalized content (ephemeral, session-scoped)

**Schema**:
```python
class PersonalizationRequest(BaseModel):
    user_id: UUID
    chapter_id: UUID
    generated_content: str
    cache_timestamp: datetime = Field(default_factory=datetime.utcnow)
```

**Storage**: In-memory cache with 1-hour TTL

**Validation Rules**:
- `generated_content`: Max 100,000 characters

**Example**:
```json
{
  "user_id": "uuid-here",
  "chapter_id": "chapter-uuid",
  "generated_content": "Simplified explanation for beginners...",
  "cache_timestamp": "2025-11-28T10:00:00Z"
}
```

---

### 10. TranslationCache

**Purpose**: Persistent cache for Urdu translations (stored in Neon Postgres)

**Schema** (SQL):
```sql
CREATE TABLE translation_cache (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    chapter_id UUID NOT NULL,
    source_content_hash VARCHAR(64) NOT NULL,  -- SHA-256 hash
    translated_content TEXT NOT NULL,
    language VARCHAR(2) CHECK (language = 'ur'),
    cached_at TIMESTAMP DEFAULT NOW(),
    UNIQUE(chapter_id, source_content_hash, language)
);

CREATE INDEX idx_chapter_hash ON translation_cache(chapter_id, source_content_hash);
```

**Pydantic Model** (Python):
```python
class TranslationCache(BaseModel):
    id: UUID
    chapter_id: UUID
    source_content_hash: str  # SHA-256 of original content
    translated_content: str
    language: Literal["ur"]
    cached_at: datetime
```

**Validation Rules**:
- `source_content_hash`: SHA-256 hex string (64 characters)
- `translated_content`: Max 200,000 characters

**Example**:
```json
{
  "id": "uuid-here",
  "chapter_id": "chapter-uuid",
  "source_content_hash": "a3f5b8c2e1d9...",
  "translated_content": "ROS 2 ایک روبوٹکس مڈل ویئر فریم ورک ہے...",
  "language": "ur",
  "cached_at": "2025-11-28T10:00:00Z"
}
```

---

## Entity Relationship Diagram

```
┌─────────────┐
│   Module    │
│  (4 total)  │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐
│    Week     │
│  (13 total) │
└──────┬──────┘
       │ 1:N
       ▼
┌─────────────┐       ┌──────────────────┐
│   Chapter   │──────▶│ EmbeddingChunk   │
│             │ 1:N   │  (Qdrant Cloud)  │
└─────────────┘       └──────────────────┘

┌──────────────┐
│ ChatSession  │ (Ephemeral)
│              │
└──────┬───────┘
       │ 1:N
       ▼
┌──────────────┐
│ ChatMessage  │ (Ephemeral)
└──────────────┘

┌───────────────┐
│ UserProfile   │ (Bonus - Neon Postgres)
└───────────────┘

┌───────────────┐
│ Translation   │ (Bonus - Neon Postgres)
│    Cache      │
└───────────────┘
```

---

## Data Validation Rules Summary

| Entity | Validation Rule | Enforcement |
|--------|----------------|-------------|
| Module | `order` in 1-4, unique | Pydantic validator |
| Week | `week_number` in 1-13, unique | Pydantic validator |
| Chapter | `content` max 50,000 chars | Pydantic validator |
| EmbeddingChunk | `embedding` exactly 1536 dims | Qdrant schema |
| ChatMessage | `content` max 2,000 chars (user) | Pydantic validator |
| UserProfile | `email` valid format, unique | SQL constraint + Pydantic |
| TranslationCache | `source_content_hash` SHA-256 | Pydantic validator |

---

## State Transitions

### ChatSession Lifecycle

```
[Created] → [Active] → [Expired (24h)] → [Deleted]
```

### PersonalizationRequest Lifecycle

```
[Generated] → [Cached (1h)] → [Expired] → [Regenerated on next request]
```

### TranslationCache Lifecycle

```
[First Request] → [Cached (permanent)] → [Invalidated on content update] → [Regenerated]
```

---

## Database Indexes

### Neon Postgres

```sql
-- UserProfile indexes
CREATE INDEX idx_user_email ON user_profiles(email);
CREATE INDEX idx_last_login ON user_profiles(last_login);

-- TranslationCache indexes
CREATE INDEX idx_chapter_hash ON translation_cache(chapter_id, source_content_hash);
```

### Qdrant Cloud

```python
# Vector index configuration (HNSW algorithm)
index_params = {
    "m": 16,  # Number of edges per node in the graph
    "ef_construct": 100  # Size of the dynamic candidate list
}
```

---

**Data Model Status**: ✅ COMPLETE

**Next Step**: Generate API contracts in `contracts/` directory
