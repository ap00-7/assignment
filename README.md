# AI-First CRM HCP Interaction Module

This project implements an AI-first Healthcare Professional (HCP) CRM interaction logging system.
It includes:

- Frontend: React + Redux
- Backend: Python + FastAPI
- AI assistant tooling modeled after a LangGraph-style agent
- Database support via SQLAlchemy with PostgreSQL / SQLite support

## Features

- Structured HCP interaction log form
- Conversational AI assistant panel for summarizing and reviewing interaction details
- Interaction editing and history
- Tool-based AI actions: log, edit, summarize, note follow-up, and extract outcomes

## Requirements

- Node 18+ and npm
- Python 3.11+
- (Optional) PostgreSQL for production-style deployment

## Setup

### Backend

```bash
cd backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env` if you want PostgreSQL support:

```bash
copy .env.example .env
```

Start backend:

```bash
uvicorn app.main:app --reload
```

### Frontend

```bash
cd frontend
npm install
npm run dev
```

## Notes

- The AI assistant integrates a LangGraph-style tool registry.
- For real Groq usage, set `GROQ_API_KEY` and optionally `GROQ_MODEL` in `backend/.env`.
- The backend defaults to SQLite for local testing.
