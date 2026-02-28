# Medical Expert AI Chat

A self-contained service with an HTTP API and React frontend for interacting with a Medical Expert AI Chat Agent. Users submit medical questions, which are processed asynchronously via an LLM, with logging and real-time statistics.

## Tech Stack

| Component | Technology |
|-----------|------------|
| Backend | FastAPI (Python), asyncio workers |
| Frontend | React (Vite) + React Router |
| LLM | OpenAI / Anthropic / Gemini / Mock (configurable) |
| Storage | In-memory (no database required) |

---

## Quick Start (Someone Cloning Your Repo)

### 1. Clone the repository

```bash
git clone https://github.com/YOUR_USERNAME/onedoc.git
cd onedoc
```

### 2. Backend setup

```bash
cd backend
python -m venv venv
source venv/bin/activate   # Windows: venv\Scripts\activate
pip install -r requirements.txt
```

### 3. Add your Gemini API key

Create a `.env` file in the **project root** (`onedoc/`, not inside `backend/`):

```bash
cd ..          # back to project root
touch .env
```

Edit `.env` and set your Gemini key:

```
LLM_PROVIDER=gemini
LLM_MODEL=gemini-flash-latest
GEMINI_API_KEY=YOUR_KEY_HERE
```

**How to get a free Gemini API key:**

1. Go to [aistudio.google.com/apikey](https://aistudio.google.com/apikey)
2. Sign in with Google
3. Click **Create API key** → choose or create a project
4. Copy the key (starts with `AIza...`) and paste it into `.env` as `GEMINI_API_KEY=...`

**Important:** Do not add quotes or spaces. Example:

```
GEMINI_API_KEY=AIzaSyAbCdEf1234567890_your_actual_key
```

### 4. Frontend setup

```bash
cd frontend
npm install
```

### 5. Run the app

**Terminal 1 — Backend:**
```bash
cd onedoc/backend
source venv/bin/activate
uvicorn main:app --host 0.0.0.0 --port 8000
```

**Terminal 2 — Frontend:**
```bash
cd onedoc/frontend
npm run dev
```

Open **http://localhost:5173** in your browser.

---

## Sharing on GitHub

### Push this project to your GitHub

1. **Create a GitHub account** (if needed): [github.com/signup](https://github.com/signup)

2. **Create a new repository:**
   - Go to [github.com/new](https://github.com/new)
   - Repository name: `onedoc`
   - Public or Private (your choice)
   - **Do not** add README, .gitignore, or license (project already has them)
   - Click **Create repository**

3. **Push your code** (from project root):

```bash
cd /Users/ofirbarel/Desktop/ofir_projects/onedoc

git init
git add .
git status   # Verify .env is NOT listed (it's ignored)
git commit -m "Initial commit: Medical Expert AI Chat"
git branch -M main
git remote add origin https://github.com/YOUR_USERNAME/onedoc.git
git push -u origin main
```

4. **Credentials when pushing:**
   - Username: your GitHub username
   - Password: use a **Personal Access Token** (not your password)
   - Create token: GitHub → Settings → Developer settings → Personal access tokens → Generate new token
   - Scopes: select `repo`
   - Or use SSH: `git@github.com:YOUR_USERNAME/onedoc.git` (add your SSH key to GitHub)

---

## Running Tests

```bash
cd backend
source venv/bin/activate
pytest tests/ -v
```

Tests use the mock LLM provider (no API key needed). All 6 tests should pass.

---

## API Endpoints

| Method | Endpoint | Description |
|--------|----------|-------------|
| `POST` | `/chat` | Submit a medical question. Body: `{"question": "..."}`. Returns `{"messageId": "uuid"}`. |
| `GET` | `/chat/{messageId}` | Get status and response. Returns `{status, answer?, error?}` — status: `processing`, `completed`, or `failed`. |
| `GET` | `/statistics` | System metrics (processed, failed, queue length, workers, etc.). |
| `GET` | `/docs` | Swagger UI (when backend is running). |

---

## Environment Variables

| Variable | Description | Default |
|----------|-------------|---------|
| `SERVER_PORT` | HTTP server port | `8000` |
| `LLM_PROVIDER` | `openai` / `anthropic` / `gemini` / `mock` | `mock` |
| `LLM_MODEL` | Model name (e.g. `gemini-flash-latest`) | `gemini-flash-latest` |
| `LLM_TEMPERATURE` | Temperature (0–1) | `0.7` |
| `LLM_MAX_TOKENS` | Max tokens per request | `1024` |
| `GEMINI_API_KEY` | Google Gemini API key (required for `gemini`) | — |
| `OPENAI_API_KEY` | OpenAI key (for `openai`) | — |
| `ANTHROPIC_API_KEY` | Anthropic key (for `anthropic`) | — |
| `RETRY_DELAY` | Seconds between retries | `2` |
| `MAX_RETRIES` | Max retry attempts | `3` |
| `WORKER_IDLE_TIMEOUT` | Worker idle timeout (seconds) | `30` |

**Never commit `.env`** — it's in `.gitignore`. Each developer creates their own `.env` with their API key.

---

## Project Structure

```
onedoc/
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── models.py
│   ├── storage.py
│   ├── queue_manager.py
│   ├── worker.py
│   ├── llm/              # OpenAI, Anthropic, Gemini, mock
│   ├── logging_utils.py
│   ├── metrics.py
│   ├── tests/
│   │   ├── conftest.py    # pytest fixtures (mock LLM)
│   │   └── test_api.py   # API endpoint tests
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── App.jsx
│   │   ├── pages/
│   │   └── api.js
│   └── package.json
├── .gitignore
└── README.md
```

---

## Troubleshooting

| Issue | Solution |
|-------|----------|
| CORS errors | Backend CORS allows `localhost:5173`. Ensure frontend runs on that port. |
| `ModuleNotFoundError` | Run from `backend/`; `pip install -r requirements.txt`. |
| API key invalid | Key from [aistudio.google.com/apikey](https://aistudio.google.com/apikey). No quotes or spaces in `.env`. |
| 429 rate limit | Free tier limits. Wait a minute or use `LLM_PROVIDER=mock` for development. |
| Port in use | Change `SERVER_PORT` in `.env` or use `--port 8001`. |
| Message not found (404) | Backend restart clears in-memory store. Avoid `--reload` during testing. |

---

## License

MIT
