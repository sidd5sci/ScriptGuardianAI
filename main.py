# main.py  (project root)
import asyncio, json
from pathlib import Path
from typing import Dict

from fastapi import FastAPI, UploadFile, File, HTTPException
from pydantic import BaseModel

# ---- make src/ importable if you didn't pip-install the project ----
import sys, pathlib
sys.path.insert(0, str(pathlib.Path(__file__).parent / "src"))

from src.ollama.ScanBee import ScanBee   # or src.ScanBee if that’s your module

# -------- initialise once -------------
bee = ScanBee()        # loads embeddings + local LLM
app = FastAPI(title="ScanBee – Script Security Auditor")

# ---------- pydantic models ----------
class ScriptIn(BaseModel):
    script: str

class VerdictOut(BaseModel):
    result: str

# ---------- helper --------------------
async def analyse_text(text: str) -> Dict:
    loop = asyncio.get_event_loop()
    return await loop.run_in_executor(None, bee.analyse, text)

# ---------- routes --------------------
@app.post("/analyze", response_model=VerdictOut)
async def analyze_script(
    body: ScriptIn | None = None,
    file: UploadFile | None = File(default=None)
):
    if body and body.script:
        script_text = body.script
    elif file:
        if not file.filename:
            raise HTTPException(400, "No file provided")
        script_text = (await file.read()).decode("utf-8", errors="ignore")
    else:
        raise HTTPException(400, "Pass JSON {'script': …} or upload a file")

    verdict = await analyse_text(script_text)
    return {"result": verdict}

@app.get("/ping")
async def ping():
    return {"msg": "pong"}

@app.get("/")
async def root():
    return {"message": "ScanBee API ready"}
