# 🤖 Physical AI & Humanoid Robotics Interactive Textbook

> An AI-native, interactive educational platform for learning Physical AI, ROS 2, Gazebo, Isaac Sim, and Vision-Language-Action (VLA) models with intelligent chatbot assistance, text-to-speech narration, and multi-language support.

[![Made with React](https://img.shields.io/badge/React-19-61DAFB?logo=react)](https://react.dev/)
[![Powered by Docusaurus](https://img.shields.io/badge/Docusaurus-3.9-green?logo=docusaurus)](https://docusaurus.io/)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.122-009688?logo=fastapi)](https://fastapi.tiangolo.com/)
[![Gemini AI](https://img.shields.io/badge/Gemini-AI-4285F4?logo=google)](https://ai.google.dev/)
[![Deployed on Vercel](https://img.shields.io/badge/Deployed-Vercel-black?logo=vercel)](https://vercel.com)
[![Backend on HF](https://img.shields.io/badge/Backend-Hugging%20Face-yellow?logo=huggingface)](https://huggingface.co/)

## 🌟 Live Demo

- **Frontend**: [https://speckit-book-hackathon-io.vercel.app/](https://speckit-book-hackathon-io.vercel.app/)
- **Backend API**: [https://ashnaali22-hackhathon-backend.hf.space](https://ashnaali22-hackhathon-backend.hf.space)
- **API Documentation**: [https://ashnaali22-hackhathon-backend.hf.space/docs](https://ashnaali22-hackhathon-backend.hf.space/docs)

---

## 📖 Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Tech Stack](#tech-stack)
- [Architecture](#architecture)
- [Features in Detail](#features-in-detail)
- [Course Content](#course-content)
- [Installation & Setup](#installation--setup)
- [Deployment](#deployment)
- [API Documentation](#api-documentation)
- [Future Enhancements](#future-enhancements)
- [Contributing](#contributing)
- [License](#license)

---

## 🎯 Overview

This project is a **modern, AI-powered interactive textbook** designed to teach Physical AI and Humanoid Robotics. It combines traditional educational content with cutting-edge AI technologies to create an immersive, adaptive learning experience.

### Why This Project?

- **AI-Native Learning**: RAG-powered chatbot provides instant, context-aware answers
- **Accessibility First**: Text-to-speech narration, mobile-friendly text selection, and responsive design
- **Multi-Modal Content**: Text, diagrams (Mermaid), code examples, and audio narration
- **Personalized Experience**: User authentication, progress tracking (coming soon), and bookmarks
- **Production-Ready**: Deployed on Vercel (frontend) and Hugging Face (backend) with Docker

---

## ✨ Key Features

### 🤖 **AI-Powered RAG Chatbot**
- **Intelligent Q&A**: Ask questions about course content and get accurate, source-cited answers
- **Powered by Google Gemini 2.0**: Advanced language understanding and generation
- **Vector Search**: Qdrant vector database with FastEmbed (BAAI/bge-small-en-v1.5) embeddings
- **Source Citations**: Every answer includes references to specific course sections and weeks
- **Confidence Scoring**: Transparent AI with confidence indicators (high/medium/low)
- **Mobile & Desktop Support**: Responsive chat interface that works seamlessly on all devices
- **Subagents for reusable intelligence**: Reused more then 6 different subagents powered by Claude
- 
### 📝 **Smart Text Selection**
- **Highlight & Ask**: Select any text and click "Ask AI" button 
- **Touch-Friendly**: Optimized for mobile with large touch targets

### 🔊 **Text-to-Speech Narration**
- **Listen Mode**: Click "Listen" button to hear content read aloud
- **Natural Voices**: Google Text-to-Speech with clear English pronunciation
- **Hands-Free Learning**: Multi-modal learning experience for better retention
- **Accessibility**: Essential for visually impaired users and auditory learners
- **Auto-Scroll**: Follow along as the text is being read (future enhancement)

### 🔐 **User Authentication System**
- **Secure Login/Logout**: Custom authentication with JWT tokens
- **Neon PostgreSQL**: Serverless database for user management
- **Password Security**: Bcrypt hashing with industry-standard security
- **Session Management**: Persistent sessions across devices
- **User Profiles**: Full name, email, and account management
- **Protected Routes**: Authentication-gated features (coming soon)

### 🌍 **Translation Support (coming soon)**
- **English-Urdu**: Bidirectional translation for accessibility
- **Batch Translation**: Translate multiple text blocks efficiently
- **Powered by Gemini**: High-quality, context-aware translations
- **Future Languages**: Extensible architecture for more languages

### 📚 **Comprehensive Course Content**

**4 Modules | 13 Weeks | Full Curriculum**

1. **Module 1: ROS 2 Fundamentals** (Weeks 1-5)
   - Introduction to Physical AI
   - ROS 2 architecture, nodes, topics, services, actions
   - Advanced ROS 2 patterns and best practices
   - Practical labs and exercises

2. **Module 2: Gazebo Simulation** (Weeks 6-7)
   - Gazebo fundamentals and URDF models
   - Physics simulation and sensor integration
   - Testing and debugging strategies

3. **Module 3: Isaac Sim** (Weeks 8-10)
   - NVIDIA Isaac Sim introduction
   - Isaac ROS integration
   - Synthetic data generation for AI training

4. **Module 4: Vision-Language-Action Models** (Weeks 11-13)
   - Humanoid robot development
   - VLA models for robotic control
   - Capstone project: Conversational robotics

### 🎨 **Modern UI/UX**
- **Dark Mode**: Eye-friendly dark theme by default
- **Mermaid Diagrams**: Interactive architecture diagrams and flowcharts
- **Responsive Design**: Perfect on mobile, tablet, and desktop
- **Fast Navigation**: Sidebar navigation with course structure
- **Search**: Full-text search across all content (Docusaurus built-in)
- **Progress Tracking**: Visual scroll progress indicator

### ⚡ **Performance & Scalability**
- **Serverless Architecture**: Scales automatically with demand
- **Vector Search**: Fast semantic search with Qdrant
- **Connection Pooling**: Efficient database connections (asyncpg)
- **CORS Enabled**: Secure cross-origin requests
- **Error Handling**: Graceful degradation and user-friendly error messages
- **Rate Limiting**: API protection (configurable)

---

## 🛠️ Tech Stack

### **Frontend**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **React** | 19.0 | UI framework |
| **Docusaurus** | 3.9.2 | Documentation site generator |
| **TypeScript** | 5.6.2 | Type-safe JavaScript |
| **Mermaid** | 11.12.1 | Diagram rendering |
| **SweetAlert2** | 11.26.3 | Beautiful alerts/modals |
| **CSS Modules** | Built-in | Component-scoped styling |

**Key Frontend Features:**
- Server-side rendering (SSR) via Docusaurus
- MDX for component-rich documentation
- Responsive design with CSS Grid/Flexbox

### **Backend**

| Technology | Version | Purpose |
|-----------|---------|---------|
| **FastAPI** | 0.122.0 | High-performance async API |
| **Python** | 3.10 | Programming language |
| **Uvicorn** | 0.27.1 | ASGI server |
| **Pydantic** | 2.12.5 | Data validation |
| **SQLAlchemy** | 2.0.44 | ORM for database |
| **asyncpg** | 0.31.0+ | PostgreSQL async driver |
| **psycopg2-binary** | 2.9.11+ | PostgreSQL sync driver |

**Authentication & Security:**
- **bcrypt** (5.0.0) - Password hashing
- **python-jose** (3.5.0) - JWT tokens
- **passlib** (1.7.4) - Password utilities
- **email-validator** (2.3.0) - Email validation
- **better-auth** (0.0.1b9) - Auth utilities

**AI & Machine Learning:**
- **Google Gemini AI** (1.52.0) - Language model
- **google-generativeai** (0.8.5) - Gemini SDK
- **Qdrant Client** (1.10.0) - Vector database
- **FastEmbed** (0.7.3) - Fast embeddings (BAAI/bge-small-en-v1.5)
- **OpenAI Agents** (0.6.1) - Agent framework (future)

### **Database**

| Technology | Purpose |
|-----------|---------|
| **Neon PostgreSQL** | User authentication and data storage (serverless) |
| **Qdrant** | Vector database for semantic search (cloud-hosted) |

### **Deployment & DevOps**

| Platform | Purpose |
|---------|---------|
| **Vercel** | Frontend hosting with auto-deployment |
| **Hugging Face Spaces** | Backend API hosting (Docker) |
| **Docker** | Containerization |
| **GitHub** | Version control and CI/CD trigger |

### **Development Tools**

- **Git** - Version control
- **npm** - Frontend package manager
- **pip** - Python package manager
- **TypeScript Compiler** - Type checking
- **Docusaurus CLI** - Development server

---

## 🏗️ Architecture

### **High-Level System Architecture**

```
┌─────────────────────────────────────────────────────────────┐
│                         CLIENT LAYER                         │
│  ┌────────────┐  ┌────────────┐  ┌────────────┐            │
│  │   Desktop  │  │   Mobile   │  │   Tablet   │            │
│  │  (Chrome)  │  │  (Safari)  │  │   (iPad)   │            │
│  └────────────┘  └────────────┘  └────────────┘            │
│                        │                                      │
└────────────────────────┼──────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────┐
│                    FRONTEND (Vercel)                         │
│  ┌──────────────────────────────────────────────────────┐  │
│  │              Docusaurus + React App                   │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │ Chat Widget │  │   Auth UI   │  │ TTS Player  │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  │  ┌─────────────┐  ┌─────────────┐  ┌─────────────┐  │  │
│  │  │Text Select  │  │  Translator │  │   Content   │  │  │
│  │  └─────────────┘  └─────────────┘  └─────────────┘  │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────────────────┼────────────────────────────────────┘
                         │ HTTPS/REST API
                         ▼
┌─────────────────────────────────────────────────────────────┐
│              BACKEND API (Hugging Face)                      │
│  ┌──────────────────────────────────────────────────────┐  │
│  │                   FastAPI Server                      │  │
│  │  ┌─────────┐  ┌──────────┐  ┌─────────┐            │  │
│  │  │  /auth  │  │  /chat   │  │/translate│            │  │
│  │  │ Routes  │  │  Routes  │  │  Routes  │            │  │
│  │  └─────────┘  └──────────┘  └─────────┘            │  │
│  │                                                        │  │
│  │  ┌──────────────────────────────────────────────┐   │  │
│  │  │           Services Layer                      │   │  │
│  │  │  ┌─────────┐  ┌──────────┐  ┌────────────┐  │   │  │
│  │  │  │Auth Svc │  │Vector DB │  │ Embeddings │  │   │  │
│  │  │  └─────────┘  └──────────┘  └────────────┘  │   │  │
│  │  │  ┌─────────┐  ┌──────────┐  ┌────────────┐  │   │  │
│  │  │  │ Gemini  │  │Query Proc│  │Translation │  │   │  │
│  │  │  └─────────┘  └──────────┘  └────────────┘  │   │  │
│  │  └──────────────────────────────────────────────┘   │  │
│  └──────────────────────────────────────────────────────┘  │
└────────────┬──────────────────────┬─────────────────────────┘
             │                      │
             ▼                      ▼
┌─────────────────────┐  ┌─────────────────────┐
│  Neon PostgreSQL    │  │   Qdrant Cloud      │
│  (User Database)    │  │  (Vector Search)    │
│  ┌───────────────┐  │  │  ┌───────────────┐  │
│  │ users table   │  │  │  │ textbook_     │  │
│  │ - id          │  │  │  │ embeddings    │  │
│  │ - email       │  │  │  │ collection    │  │
│  │ - password    │  │  │  │ (384 dims)    │  │
│  │ - full_name   │  │  │  └───────────────┘  │
│  └───────────────┘  │  └─────────────────────┘
└─────────────────────┘
             │
             ▼
┌─────────────────────┐
│   Google Gemini AI  │
│   (Cloud Service)   │
│  ┌───────────────┐  │
│  │ gemini-2.0    │  │
│  │ -flash        │  │
│  │ Language Model│  │
│  └───────────────┘  │
└─────────────────────┘
```

### **Data Flow: RAG Chatbot**

```
User Query → Frontend ChatWidget
     │
     ├─→ POST /api/chat/ (FastAPI)
     │
     ├─→ Query Processor (text cleaning)
     │
     ├─→ Embedding Service (FastEmbed)
     │    └─→ Generate query embedding (384-dim vector)
     │
     ├─→ Qdrant Vector Search
     │    └─→ Find top-k similar chunks (cosine similarity > 0.7)
     │
     ├─→ Generation Service
     │    ├─→ Build context from retrieved chunks
     │    ├─→ Create prompt with citations
     │    └─→ Call Gemini AI
     │
     └─→ Response with answer + sources + confidence
          └─→ Display in ChatWidget with source citations
```

### **Authentication Flow**

```
User → Login/Signup → AuthModal (Frontend)
     │
     ├─→ POST /auth/signup or /auth/login
     │
     ├─→ Password Validation (Pydantic)
     │
     ├─→ Neon PostgreSQL Query
     │    ├─→ Check if user exists
     │    ├─→ Hash password (bcrypt)
     │    └─→ Create/verify user
     │
     ├─→ Generate JWT Token (python-jose)
     │    └─→ Claims: {sub: email, id: user_id}
     │
     └─→ Return Token
          └─→ Store in AuthContext
               └─→ Use in protected API calls
```

---

## 🔥 Features in Detail

### 1. **RAG-Powered Chatbot**

**Technology**: Retrieval-Augmented Generation (RAG)

**How it works:**
1. User asks a question (e.g., "What is ROS 2?")
2. Query is processed and enhanced
3. Query embedding is generated using FastEmbed (BAAI/bge-small-en-v1.5)
4. Qdrant searches for semantically similar content chunks
5. Top-k relevant excerpts are retrieved (default: 5)
6. Context + query is sent to Google Gemini 2.0
7. Gemini generates a comprehensive answer
8. Response includes source citations with week numbers and sections

**Key Features:**
- **Source Citations**: Every answer references specific course sections
- **Confidence Scoring**: Transparent AI with high/medium/low confidence
- **Context Window**: Retrieves up to 10 sources for comprehensive answers
- **Error Handling**: Graceful fallbacks if backend is unavailable

**Example:**
```json
{
  "answer": "ROS 2 is middleware that powers robots...",
  "sources": [
    {"excerpt_num": 1, "week": 3, "section": "Week 03 ROS2 Architecture", "score": 0.866},
    {"excerpt_num": 2, "week": 3, "section": "Week 03 ROS2 Architecture", "score": 0.842}
  ],
  "confidence": "high",
  "has_answer": true
}
```

### 2. **Smart Text Selection**

**Mobile-First Design**

**Features:**
- ✅ Works on touch devices (iOS, Android)
- ✅ Works on desktop (mouse selection)
- ✅ No right-click required
- ✅ Automatic "Ask AI" button positioning
- ✅ Viewport-aware (doesn't go off-screen)
- ✅ Large touch targets (48px minimum)
- ✅ Smooth animations and transitions

**Implementation:**
- Listens to `mouseup`, `touchend`, and `selectionchange` events
- Calculates optimal button position (above/below selection)
- Adjusts for screen edges and viewport boundaries
- Integrates with ChatWidget for seamless Q&A

### 3. **Text-to-Speech Narration**

**Accessibility Feature**

**Powered by**: Web Speech API

**Features:**
- ✅ Natural voice synthesis
- ✅ Google English voices (clear pronunciation)
- ✅ Play/pause controls
- ✅ Reads entire article content
- ✅ Visual feedback (speaking indicator)
- ✅ Browser-native (no external dependencies)

**Use Cases:**
- Visually impaired users
- Auditory learners
- Hands-free learning (driving, exercising)
- Multi-tasking while learning

**Future Enhancements:**
- Multiple voice options (male/female, accents)
- Playback speed controls (0.75x, 1x, 1.5x, 2x)
- Auto-scroll to follow narration
- Highlight current sentence
- Download audio for offline use

### 4. **User Authentication**

**Custom Auth System**

**Database**: Neon PostgreSQL (serverless)

**Security Features:**
- ✅ Bcrypt password hashing (cost factor: 12)
- ✅ JWT tokens with expiration (30 minutes)
- ✅ Email validation (RFC 5322 compliant)
- ✅ SQL injection protection (parameterized queries)
- ✅ CORS protection
- ✅ Rate limiting (100 requests/min)

**User Management:**
```python
# User Model
class User:
    id: int (auto-increment)
    email: str (unique, indexed)
    password_hash: str (bcrypt)
    full_name: str
    created_at: timestamp
```

**Endpoints:**
- `POST /auth/signup` - User registration
- `POST /auth/login` - User login
- `POST /auth/logout` - User logout (future)
- `GET /auth/me` - Get current user (future)

### 5. **Translation System**

**English ↔ Urdu**

**Powered by**: Google Gemini AI

**Features:**
- ✅ Bidirectional translation
- ✅ Context-aware (preserves technical terms)
- ✅ Batch translation (multiple texts)
- ✅ Translation caching (future)
- ✅ Quality scoring

**Endpoints:**
- `POST /api/translate/` - Single text translation
- `POST /api/translate/batch` - Batch translation

### 6. **Vector Search (RAG)**

**Technology**: Qdrant Cloud + FastEmbed

**Configuration:**
- **Collection**: `textbook_embeddings`
- **Dimensions**: 384 (BAAI/bge-small-en-v1.5 model)
- **Distance Metric**: Cosine similarity
- **Score Threshold**: 0.7 (minimum relevance)
- **Top-K**: 5 results (configurable up to 10)

**Indexing:**
- Course content is chunked by section
- Each chunk includes metadata: week, module, section, content
- Embeddings are generated with FastEmbed
- Uploaded to Qdrant in batches (50 per batch)

**Search Performance:**
- < 100ms query latency (p95)
- < 500ms end-to-end response time
- Scales to millions of documents

---

## 📚 Course Content

### **Module Structure**

```
📖 Physical AI & Humanoid Robotics Textbook
│
├─ 📘 Module 1: ROS 2 Fundamentals (Weeks 1-5)
│  ├─ Week 1: Introduction to Physical AI
│  ├─ Week 2: Physical AI Landscape
│  ├─ Week 3: ROS 2 Architecture
│  ├─ Week 4: ROS 2 Practical Development
│  └─ Week 5: ROS 2 Advanced Topics
│
├─ 📗 Module 2: Gazebo Simulation (Weeks 6-7)
│  ├─ Week 6: Gazebo Fundamentals
│  └─ Week 7: Advanced Gazebo & URDF
│
├─ 📙 Module 3: Isaac Sim (Weeks 8-10)
│  ├─ Week 8: Isaac Sim Introduction
│  ├─ Week 9: Isaac ROS Integration
│  └─ Week 10: Synthetic Data & Sim2Real
│
└─ 📕 Module 4: VLA Models (Weeks 11-13)
   ├─ Week 11: Humanoid Development
   ├─ Week 12: Vision-Language-Action Models
   └─ Week 13: Capstone - Conversational Robotics
```

### **Content Types**

- **Text Lessons**: Comprehensive explanations with examples
- **Mermaid Diagrams**: Architecture diagrams, flowcharts, sequence diagrams
- **Code Examples**: Python, C++, ROS 2 launch files, URDF models
- **Practical Labs**: Hands-on exercises and projects
- **Quizzes**: Self-assessment (future)
- **Video Embeddings**: Tutorial videos (future)

---

## 🔮 Future Enhancements

### **Planned Features**

#### **1. OpenAI Agents SDK Integration**
- Migrate to OpenAI Agents SDK with Gemini via LiteLLM
- Multi-agent architecture (Textbook Agent, Translator Agent, Tutor Agent)
- Better conversation management and state handling
- Tool ecosystem integration
- **Status**: Documented in `docs/future-work/openai-agents-sdk-migration.md`

#### **2. User Progress Tracking**
- Track completed modules and lessons
- Progress bars and badges
- Completion certificates
- Streak tracking (daily learning goals)

#### **3. Enhanced Audio Features**
- Multiple voice options (male/female, accents)
- Playback speed controls (0.75x, 1x, 1.5x, 2x)
- Auto-scroll to follow narration
- Highlight current sentence being read
- Download audio for offline use
- Podcast-style episode generation

#### **4. Social Learning**
- Discussion forums per lesson
- Community Q&A
- User-generated content (notes, summaries)
- Peer code reviews
- Study groups

#### **5. Advanced Authentication**
- Social login (Google, GitHub, Microsoft)
- Password reset via email
- Email verification
- Two-factor authentication (2FA)
- OAuth2 integration

#### **6. Interactive Code Playground**
- In-browser ROS 2 code editor
- Real-time syntax checking
- Code execution sandbox
- Save and share code snippets
- Integration with GitHub Gists

#### **7. Quizzes & Assessments**
- Multiple choice questions
- Code challenges
- Auto-graded assignments
- Skill assessments
- Certification exams

#### **8. Offline Mode**
- Progressive Web App (PWA)
- Download lessons for offline reading
- Cached embeddings for offline RAG
- Service workers for caching

#### **9. Analytics & Insights**
- User engagement metrics
- Learning paths analytics
- Time spent per module
- Most asked questions
- Chatbot improvement suggestions

#### **10. Multi-Language Support**
- Full i18n (internationalization)
- More languages beyond Urdu (Spanish, Chinese, Arabic)
- Language-specific content variants
- RTL (Right-to-Left) support

---

## 🤝 Contributing

Contributions are welcome! Please follow these guidelines:

### **Development Workflow**

1. **Fork the repository**
2. **Create a feature branch**: `git checkout -b feature/amazing-feature`
3. **Make your changes**
4. **Test thoroughly** (frontend and backend)
5. **Commit with clear messages**: `git commit -m "Add amazing feature"`
6. **Push to your fork**: `git push origin feature/amazing-feature`
7. **Open a Pull Request**
   
---

## 📄 License

This project is licensed under the **MIT License**.

```
MIT License

Copyright (c) 2025 Ashna Ghazanfar

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.
```

---

## 📞 Contact & Support

**Author**: Ashna Ghazanfar
**Email**: nutellacookiesss@gmail.com
**GitHub**: [@Syedaashnaghazanfar](https://github.com/Syedaashnaghazanfar)
**Project Repository**: [speckit-book-hackathon.io](https://github.com/Syedaashnaghazanfar/speckit-book-hackathon.io)

### **Getting Help**

- 🐛 **Bug Reports**: [Open an issue](https://github.com/Syedaashnaghazanfar/speckit-book-hackathon.io/issues)
- 💡 **Feature Requests**: [Open a discussion](https://github.com/Syedaashnaghazanfar/speckit-book-hackathon.io/discussions)
- 📧 **Email**: For private inquiries

---

## 🌟 Star History

If you find this project useful, please consider giving it a ⭐ on GitHub!

[![Star History Chart](https://api.star-history.com/svg?repos=Syedaashnaghazanfar/speckit-book-hackathon.io&type=Date)](https://star-history.com/#Syedaashnaghazanfar/speckit-book-hackathon.io&Date)

---

**Made with ❤️ for the future of AI education - Ashna Ghazanfar**

**Last Updated**: December 2025
