# NexusFlow — Agentic AI Multi-Agent Orchestration System

A clean, base-level **Multi-Agent AI System** featuring four autonomous collaborating agents (**Planner**, **Researcher**, **Builder**, and **Reviewer**) with a live visual orchestration studio. Built to push directly to GitHub and deploy a live shareable link on **Vercel** or **Render** in under 2 minutes.

## Architecture & Agent Pipeline

1. **01 • Planner Agent (`Task Decomposer`)**: Breaks any high-level objective into structured milestones, tool calls, and acceptance criteria.
2. **02 • Researcher Agent (`Domain Synthesizer`)**: Evaluates architecture patterns, algorithmic bounds, and edge cases.
3. **03 • Builder Agent (`Code & Artifact Synthesizer`)**: Generates modular implementation code and configuration satisfying the plan.
4. **04 • Reviewer Agent (`Critic & QA Verifier`)**: Audits the implementation against the Planner's criteria and computes a QA score.

Supports two execution modes:
- **Simulated Engine Mode (Default • Zero Config)**: Works out-of-the-box on your live Vercel/Render URL without requiring visitors or recruiters to enter an API key.
- **Live Gemini API Mode (`gemini-3.8-flash`)**: Uses the official Google GenAI SDK (`google-genai` / `@google/genai`) via `/api/orchestrate` or browser API key.

## Repository Structure

```text
agentic-multiagent-studio/
├── index.html           # Self-contained Multi-Agent Studio UI (works standalone & with backend)
├── agents.py            # Modular Python 4-agent orchestrator + CLI runner (google-genai)
├── server.py            # FastAPI backend serving index.html and POST /api/orchestrate
├── api/
│   └── orchestrate.js   # Vercel Serverless Function (@google/genai)
├── vercel.json          # Vercel zero-config routing
├── package.json         # Node dependencies for Vercel serverless API
├── render.yaml          # Render Blueprint for 1-click Python web service deploy
├── requirements.txt     # Python dependencies for Render & local execution
└── .env.example         # Environment variable template
```

## Quick Start (Local)

### Option A: Open UI Instantly
Open `index.html` in any browser, or serve locally:
```bash
python -m http.server 8000
```

### Option B: Run Full Python FastAPI Server
```bash
pip install -r requirements.txt
uvicorn server:app --reload --port 8000
```
Then visit `http://localhost:8000` or run the CLI orchestrator directly:
```bash
python agents.py "Design a rate-limiter middleware in FastAPI"
```

## Deploy a Live Link (Vercel or Render)

### 1. Deploy on Vercel (Recommended for Instant Live Link)
1. Push this folder to a new GitHub repository.
2. Go to [Vercel New Project](https://vercel.com/new) and import your repository.
3. Click **Deploy** (no build command needed; `vercel.json` serves `index.html` and mounts `/api/orchestrate`).
4. *(Optional)* Add `GEMINI_API_KEY` under **Settings → Environment Variables** in Vercel for server-side live Gemini calls.

### 2. Deploy on Render (Python FastAPI Backend + UI)
1. Push this folder to a GitHub repository.
2. Go to [Render Dashboard](https://dashboard.render.com), click **New → Web Service**, and connect your repository.
3. Set **Build Command**: `pip install -r requirements.txt`
4. Set **Start Command**: `uvicorn server:app --host 0.0.0.0 --port $PORT`
5. *(Optional)* Add `GEMINI_API_KEY` in Environment Variables, then click **Create Web Service**.
