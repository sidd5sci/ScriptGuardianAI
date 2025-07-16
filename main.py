"""FastAPI entry point for script Guardian  - now backed by the revamped **Guardian**
class that can talk to either Ollama or LM Studio.

Environment variables
---------------------
LLM_BACKEND              "ollama" (default) | "lmstudio"
SECSCAN_MODEL_OLLAMA     model name when backend is ollama
SECSCAN_MODEL_LMS        model name when backend is lmstudio
SECSCAN_T                temperature (float, default 0.0)

Run
---
python -m uvicorn main:app --reload --port 8080

$ uvicorn main:app --reload --port 8080
$ uvicorn main:app --reload
"""
from __future__ import annotations

import asyncio
import os
from pathlib import Path
from typing import Any, Dict, Optional

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel

import sys
import pathlib

# add src to PYTHONPATH
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

from src.lm.Guardian import Guardian  # noqa: E402  pylint: disable=wrong-import-position

# ---------------------------------------------------------------------------
# Guardian initialisation (done once at startup)
# ---------------------------------------------------------------------------
BACKEND = os.getenv("LLM_BACKEND", "ollama").lower()
TEMPERATURE = float(os.getenv("SECSCAN_T", "0"))

bee = Guardian(backend=BACKEND, temperature=TEMPERATURE)

# ---------------------------------------------------------------------------
# FastAPI setup
# ---------------------------------------------------------------------------
app = FastAPI(title="Script Guardian - Script Security Auditor")

# serve static HTML/JS assets (optional UI)
static_dir = Path(__file__).parent / "static"
if static_dir.exists():
    app.mount("/static", StaticFiles(directory=static_dir, html=True), name="static")

# CORS for local dev / web UI
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------------------------------------------------------------------------
# Pydantic models
# ---------------------------------------------------------------------------
class ScriptIn(BaseModel):
    script: str


class VerdictOut(BaseModel):
    result: Any


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------
async def analyse_text(text: str, script_type: str) -> Dict[str, Any]:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, bee.analyse_code, text, script_type)


# ---------------------------------------------------------------------------
# Routes
# ---------------------------------------------------------------------------
@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("static/index.html")

@app.post("/analyze", response_model=VerdictOut)
async def analyze_script(request: Request, file: UploadFile | None = File(None)):
    script_text = None
    script_type = None
    
    try:
        # Attempt to parse JSON body first
        body = await request.json()
        script_text = body.get("script", "").strip()
        script_type = body.get("scriptType", "powershell")
        if script_text:
            print("[analyze_script] Using script from JSON body")
    except Exception:
        # JSON body not present or unreadable
        pass

    # If no script in JSON, try file upload
    if not script_text and file:
        script_text = (await file.read()).decode("utf-8", errors="ignore").strip()
        print("[analyze_script] Using script from uploaded file")

    if not script_text:
        raise HTTPException(400, "No script provided via JSON body or uploaded file")

    print(f"[analyze_script] Script length: {len(script_text)} characters")
    verdict = await analyse_text(script_text, script_type)
    print(f"[analyze_script] Analysis complete. Verdict: {verdict.get('script', 'unknown')}")
    return {"result": verdict}

@app.get("/ping")
async def ping():
    return {"msg": "pong"}
