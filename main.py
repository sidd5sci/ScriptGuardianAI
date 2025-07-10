# main.py  (project root)
import asyncio, json
from pathlib import Path
from typing import Dict
from typing import Any

from fastapi import FastAPI, UploadFile, File, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from pydantic import BaseModel
from typing import Optional
from fastapi.staticfiles import StaticFiles
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))
from src.lm.Guardian import Guardian   



# -------- initialise once -------------
bee = Guardian()        # loads embeddings + local LLM

DEFAULT_PROMPT_PATH_PS1 = Path("src/lm/prompts/powershell/prompt_11.md")
DEFAULT_PROMPT_PATH_GROOVY = Path("src/lm/prompts/groovy/prompt_9.md")

if not DEFAULT_PROMPT_PATH_PS1.exists() and not DEFAULT_PROMPT_PATH_GROOVY.exists():
    raise FileNotFoundError(f"Prompt file not found: {DEFAULT_PROMPT_PATH_PS1}, {DEFAULT_PROMPT_PATH_GROOVY}")

bee.prompt = DEFAULT_PROMPT_PATH.read_text(encoding="utf-8")

app = FastAPI(title="ScanBee – Script Security Auditor")

app.mount("/static", StaticFiles(directory="static", html=True), name="static")

# Add CORS middleware to allow requests from anywhere (or restrict to specific origins)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # ← OK for local dev
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ---------- pydantic models ----------
class ScriptIn(BaseModel):
    script: str

class VerdictOut(BaseModel):
    result: Any

# ---------- helper --------------------
async def analyse_text(text: str) -> Dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, bee.analyse, text)

# ---------- routes --------------------

@app.get("/", include_in_schema=False)
async def serve_index():
    return FileResponse("static/index.html")

@app.post("/analyze", response_model=VerdictOut)
async def analyze_script(request: Request, file: UploadFile = File(None)):
    content_type = request.headers.get("content-type", "")

    if "application/json" in content_type:
        body = await request.json()
        if "script" not in body:
            raise HTTPException(400, "Missing 'script' in JSON")
        script_text = body["script"]

    elif "multipart/form-data" in content_type:
        if not file:
            raise HTTPException(400, "No file uploaded")
        script_text = (await file.read()).decode("utf-8", errors="ignore")

    else:
        raise HTTPException(400, "Unsupported content type")

    instrumented_code = bee.with_line_markers(script_text)
    verdict = await analyse_text(instrumented_code)
    return {"result": verdict}

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/")
async def root():
    return {"message": "ScanBee API ready"}
