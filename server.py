"""
FastAPI Web Server for Render Deployment (`uvicorn server:app --host 0.0.0.0 --port $PORT`)
Serves both the interactive `index.html` studio and `POST /api/orchestrate`.
"""

import os
from pathlib import Path
from fastapi import FastAPI
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel
from agents import MultiAgentOrchestrator

app = FastAPI(title="NexusFlow Multi-Agent Studio", version="1.0.0")
BASE_DIR = Path(__file__).resolve().parent


class OrchestrateRequest(BaseModel):
    objective: str
    apiKey: str | None = None


@app.get("/")
async def serve_ui():
    return FileResponse(BASE_DIR / "index.html")


@app.get("/health")
async def health():
    return {"status": "ok", "service": "nexusflow-multiagent-studio"}


@app.post("/api/orchestrate")
async def orchestrate_endpoint(payload: OrchestrateRequest):
    orchestrator = MultiAgentOrchestrator(api_key=payload.apiKey)
    outputs = orchestrator.run_pipeline(payload.objective)
    return JSONResponse({"status": "completed", "outputs": outputs})
