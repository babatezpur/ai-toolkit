# AI Toolkit

A Flask REST API that wraps OpenAI's GPT-4o-mini to provide AI-powered features — random facts, quotes, and multi-turn Q&A conversations. The backend adds authentication, rate limiting, saved items, and trending topic tracking on top of the raw AI capabilities.

## Tech Stack

- **Backend:** Python 3 / Flask
- **Database:** PostgreSQL (with Flask-SQLAlchemy ORM and Flask-Migrate for migrations)
- **Auth:** JWT-based authentication (Flask-JWT-Extended)
- **Validation:** Marshmallow schemas for request validation and response serialization
- **AI Provider:** OpenAI API (GPT-4o-mini with JSON mode)
- **Server:** Gunicorn (production)

## Features

- **Random Facts** — Provide a topic and get 5 AI-generated facts. Supports optional instructions (e.g. "beginner friendly").
- **Quotes** — Provide a topic and get 5 AI-generated quotes with authors. Supports optional instructions (e.g. "from athletes only").
- **Q&A Conversations** — Start a conversation and ask follow-up questions. Conversations support up to 5 user messages and are stored in-memory with a 30-minute TTL.
- **Saved Items** — Save favourite facts or quotes. View, filter by category, or delete them.
- **Trending Topics** — See the top 10 most searched topics across all users, with optional filtering by feature (facts/quotes).
- **Rate Limiting** — 20 AI requests per user per day (facts + quotes + Q&A messages all count). Resets daily.

## API Endpoints

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Create a new account | No |
| POST | `/auth/login` | Log in and get a JWT token | No |
| POST | `/facts/` | Generate 5 facts on a topic | Yes |
| POST | `/quotes/` | Generate 5 quotes on a topic | Yes |
| POST | `/conversation/start` | Start a new Q&A conversation | Yes |
| POST | `/conversation/message` | Send a message in a conversation | Yes |
| GET | `/conversation/conversations` | List all active conversations | Yes |
| GET | `/conversation/conversations/<id>` | Get a specific conversation | Yes |
| POST | `/favourites/` | Save a fact or quote | Yes |
| GET | `/favourites/` | Get saved items (optional `?category=fact\|quote`) | Yes |
| DELETE | `/favourites/<id>` | Delete a saved item | Yes |
| GET | `/trending/` | Get top 10 trending topics (optional `?feature=facts\|quotes`) | Yes |

## Project Structure

```
ai-toolkit/
├── app/
│   ├── __init__.py           # App factory, extension init, blueprint registration
│   ├── config.py             # Configuration (DB URL, JWT secret, OpenAI key)
│   ├── models/               # SQLAlchemy models (User, SavedItem, SearchedItem)
│   ├── routes/               # Route blueprints (auth, facts, quotes, conversation, favourites, trending)
│   ├── services/             # Business logic (OpenAI calls, rate limiting, conversation store)
│   ├── schemas/              # Marshmallow schemas for validation and serialization
│   ├── prompts/              # Prompt templates for OpenAI
│   ├── middlewares/          # JWT auth decorator
│   └── errors/               # Custom exceptions and global error handlers
├── migrations/               # Alembic migration files
├── requirements.txt
├── run.py                    # Entry point
├── .env.example              # Template for environment variables
└── CLAUDE.md                 # Project plan and architecture docs
```

## Architecture

```
Request → Routes (HTTP layer) → Services (business logic, OpenAI) → Models (DB)
                               → Schemas (validate input, format output)
                               → Prompts (prompt templates for OpenAI)
```

Routes are thin — they handle HTTP concerns only. All business logic lives in the services layer.

## Setup (Local Development)

1. **Clone and create a virtual environment:**
   ```bash
   git clone https://github.com/<your-username>/ai-toolkit.git
   cd ai-toolkit
   python3 -m venv venv
   source venv/bin/activate
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up environment variables:**
   ```bash
   cp .env.example .env
   # Edit .env with your actual values:
   #   DATABASE_URL=postgresql://username:password@localhost:5432/ai_toolkit
   #   JWT_SECRET_KEY=your-secret-key
   #   OPENAI_API_KEY=sk-your-key
   ```

4. **Set up the database:**
   ```bash
   createdb ai_toolkit
   flask db upgrade
   ```

5. **Run the development server:**
   ```bash
   python run.py
   ```
   The API will be available at `http://localhost:5000`.

## Deployment

The app is deployed on **Render** (free tier).

- **Server:** Gunicorn
- **Build command:** `pip install -r requirements.txt && flask db upgrade` (installs dependencies and runs migrations on every deploy)
- **Database:** Render managed PostgreSQL (free tier, Singapore region)
- **Environment variables** (`DATABASE_URL`, `JWT_SECRET_KEY`, `OPENAI_API_KEY`) are configured in Render's dashboard
- **Auto-deploy:** Every push to `main` triggers a new deployment
- **Live API:** https://ai-toolkit-9ycz.onrender.com

> **Note:** On the free tier, the service sleeps after 15 minutes of inactivity and takes 30-60 seconds to wake up on the first request.

## Error Handling

The API uses centralized custom exceptions with consistent error responses:

| Status Code | Exception | Meaning |
|-------------|-----------|---------|
| 400 | `BadRequestError` | Invalid input or missing fields |
| 401 | `UnauthorizedError` | Missing or invalid token |
| 403 | `ForbiddenError` | Access denied |
| 404 | `NotFoundError` | Resource not found |
| 409 | `ConflictError` | Duplicate or conflicting data |
| 429 | `RateLimitError` | Daily request limit reached |
| 500 | `OpenAIError` | AI service error |

All error responses follow the format:
```json
{ "error": "Error message here" }
```
