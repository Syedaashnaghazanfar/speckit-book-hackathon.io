# Developer Quickstart: Physical AI & Humanoid Robotics Textbook

**Date**: 2025-11-28
**Phase**: 1 (Design & Contracts)

## Prerequisites

- **Node.js**: 18+ ([Download](https://nodejs.org/))
- **Python**: 3.11+ ([Download](https://www.python.org/downloads/))
- **Git**: Latest version
- **API Keys** (obtain before starting):
  - OpenAI API Key ([Get key](https://platform.openai.com/api-keys))
  - Qdrant Cloud API Key ([Sign up](https://cloud.qdrant.io/))
  - Gemini API Key ([Get key](https://aistudio.google.com/app/apikey))
  - Neon Postgres URL (Bonus) ([Sign up](https://neon.tech/))

## Quick Start (5 Minutes)

### 1. Clone Repository

```bash
git clone https://github.com/your-org/hackhathon-book.git
cd hackhathon-book
git checkout 001-physical-ai-textbook
```

### 2. Environment Setup

```bash
# Backend
cp backend/.env.example backend/.env
# Fill in: OPENAI_API_KEY, QDRANT_API_KEY, QDRANT_URL, GEMINI_API_KEY

# Frontend
cp frontend/.env.example frontend/.env
# Fill in: REACT_APP_API_URL (e.g., http://localhost:8000)
```

### 3. Backend Setup

```bash
cd backend
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# macOS/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt

# Generate embeddings (one-time, ~10-15 minutes)
python scripts/generate_embeddings.py

# Start backend
uvicorn src.main:app --reload --port 8000
```

**Backend running at**: http://localhost:8000
**API docs**: http://localhost:8000/docs

### 4. Frontend Setup (New Terminal)

```bash
cd frontend
npm install
npm start
```

**Frontend running at**: http://localhost:3000

## Project Structure

```
hackhathon-book/
├── backend/               # FastAPI backend
│   ├── src/
│   │   ├── main.py       # FastAPI app entry point
│   │   ├── api/          # Route handlers
│   │   ├── services/     # Business logic
│   │   └── models/       # Pydantic schemas
│   ├── tests/            # pytest tests
│   ├── scripts/
│   │   └── generate_embeddings.py
│   └── requirements.txt
│
├── frontend/             # Docusaurus site
│   ├── docs/             # MDX content
│   │   ├── module-1-ros2/
│   │   ├── module-2-gazebo/
│   │   ├── module-3-isaac/
│   │   └── module-4-vla/
│   ├── src/
│   │   ├── components/   # React components (ChatWidget, etc.)
│   │   └── css/          # Purple/neon theme
│   └── package.json
│
└── specs/                # Feature documentation
    └── 001-physical-ai-textbook/
        ├── spec.md
        ├── plan.md
        ├── research.md
        ├── data-model.md
        └── quickstart.md
```

## Development Workflow

### Adding New Content

1. Create MDX file in `frontend/docs/module-X/`
2. Add to sidebar in `frontend/sidebars.js`
3. Regenerate embeddings: `python backend/scripts/generate_embeddings.py`
4. Restart backend

### Testing

```bash
# Backend tests
cd backend
pytest tests/ -v

# Frontend tests
cd frontend
npm test

# E2E tests (Playwright)
npx playwright test
```

### Building for Production

```bash
# Frontend (static build)
cd frontend
npm run build
# Output: frontend/build/

# Backend (containerize)
cd backend
docker build -t textbook-backend .
```

## Deployment

### Frontend → GitHub Pages

```bash
cd frontend
npm run build
npm run deploy  # Pushes to gh-pages branch
```

### Backend → Vercel

```bash
cd backend
vercel deploy
```

## Troubleshooting

### "Module not found" errors
```bash
# Backend
pip install -r requirements.txt --force-reinstall

# Frontend
rm -rf node_modules package-lock.json
npm install
```

### Embedding generation fails
- Check OpenAI API key is valid
- Ensure content files exist in `frontend/docs/`
- Verify Qdrant Cloud connection: `curl https://your-cluster.qdrant.io/collections`

### Chat not responding
- Confirm backend is running: http://localhost:8000/health
- Check Gemini API key is set
- Verify CORS settings in `backend/src/middleware/cors.py`

## Next Steps

1. Review constitution: `.specify/memory/constitution.md`
2. Read feature spec: `specs/001-physical-ai-textbook/spec.md`
3. Check implementation plan: `specs/001-physical-ai-textbook/plan.md`
4. Run `/sp.tasks` to generate task breakdown
5. Start implementing following TDD workflow

## Useful Commands

```bash
# Start all services (requires tmux or separate terminals)
# Terminal 1:
cd backend && uvicorn src.main:app --reload

# Terminal 2:
cd frontend && npm start

# Run tests
pytest backend/tests/
npm test --prefix frontend

# Format code
black backend/src/
npm run format --prefix frontend

# Lint
pylint backend/src/
npm run lint --prefix frontend
```

## API Endpoints (Local Development)

- `POST /api/chat` - Main chat endpoint
- `POST /api/chat/selection` - Text selection query
- `GET /api/health` - Health check
- `POST /api/auth/signup` - User signup (Bonus)
- `POST /api/personalize` - Content personalization (Bonus)
- `POST /api/translate` - Urdu translation (Bonus)
- `GET /docs` - OpenAPI/Swagger documentation

## Environment Variables Reference

### Backend `.env`

```
OPENAI_API_KEY=sk-...
QDRANT_API_KEY=...
QDRANT_URL=https://your-cluster.qdrant.io
GEMINI_API_KEY=...
NEON_DATABASE_URL=postgres://...  # Bonus feature
AUTH_SECRET_KEY=...  # Bonus feature
```

### Frontend `.env`

```
REACT_APP_API_URL=http://localhost:8000
```

**Quickstart Status**: ✅ COMPLETE
