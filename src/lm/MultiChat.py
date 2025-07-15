"""Guardian - static analysis driver that can switch between **Ollama** and
**LM Studio** back ends.

* Pick the runtime via ``LLM_BACKEND`` env var (``"ollama"`` | ``"lmstudio"``)
  or the ``backend=`` ctor arg.
* Models can differ per platform:

  * ``SECSCAN_MODEL_OLLAMA`` → model name for Ollama
  * ``SECSCAN_MODEL_LMS``    → model name for LM Studio

Fallback defaults are provided for both.

Example
-------
```bash
export LLM_BACKEND=ollama                 # or lmstudio
export SECSCAN_MODEL_OLLAMA="gemma:2b"   # only used when backend == ollama

python guardian.py scripts/myscript.ps1
```
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage,
)
from src.lm.Ollama import OllamaChat
from src.lm.LMStudio import LMStudioChat

# ---------------------------------------------------------------------------
# Back‑end & model configuration
# ---------------------------------------------------------------------------
BACKEND = os.getenv("LLM_BACKEND", "ollama").lower()  # "ollama" | "lmstudio"

DEFAULT_OLLAMA_MODEL = "hf.co/reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled:latest"
DEFAULT_LMS_MODEL = "claude-3.7-sonnet-reasoning-gemma3-12b"

OLLAMA_MODEL = os.getenv("SECSCAN_MODEL_OLLAMA", DEFAULT_OLLAMA_MODEL)
LMS_MODEL = os.getenv("SECSCAN_MODEL_LMS", DEFAULT_LMS_MODEL)

TEMPERATURE = float(os.getenv("SECSCAN_T", "0"))


class MultiChat:
    """Analyse PowerShell & Groovy scripts for security issues using an LLM."""

    def __init__(self, backend: str = BACKEND, temperature: float = TEMPERATURE):
        self.backend = backend
        self.temperature = temperature

        if backend == "ollama":
            self.llm = OllamaChat(model=OLLAMA_MODEL, temperature=temperature)
        elif backend == "lmstudio":
            self.llm = LMStudioChat(model=LMS_MODEL, temperature=temperature)
        else:
            raise ValueError("backend must be 'ollama' or 'lmstudio'")

        # --- parser & prompt paths ---
        self.prompt_ps1 = Path("src/lm/prompts/powershell/prompt_11.md")
        self.prompt_groovy = Path("src/lm/prompts/groovy/prompt_9.md")

        if not (self.prompt_ps1.is_file() and self.prompt_groovy.is_file()):
            sys.exit("ERR: prompt files missing")

        self._line_map: Dict[int, bool] = {}

    # ------------------------------ chat glue -----------------------------
    @staticmethod
    def _to_chat_messages(lst: List[Dict[str, str]]):
        role_map = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage}
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    # ------------------------------ analysis -----------------------------
    def analyse(self, prompt: str) -> Dict[str, Any]:
        chat_messages = self._to_chat_messages([
            {"role": "user", "content": prompt},
        ])
        response = self.llm.invoke(chat_messages)
        raw_json = self._extract_json(response.content) or {}
        return raw_json

    # ------------------------- file & folder helpers ----------------------
    def analyse_file(self, path: Path) -> Dict[str, Any]:
        code = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix.lower() == ".ps1":
            prompt_tpl = self.prompt_ps1.read_text(encoding="utf-8")
        elif path.suffix.lower() == ".groovy":
            prompt_tpl = self.prompt_groovy.read_text(encoding="utf-8")
        else:
            raise ValueError("Unsupported file type")

        instrumented = self.with_line_markers(code)
        prompt = f"{prompt_tpl}\n\n<BEGIN CODE>\n{self.escape_braces(instrumented)}\n<END CODE>"
        return self.analyse(prompt)

    # ----------------------------- utilities -----------------------------
    def with_line_markers(self, code: str) -> str:
        self._original_lines = code.splitlines()
        self._line_map = {}
        output_lines = []
        for i, line in enumerate(self._original_lines, start=1):
            self._line_map[i] = line.strip().startswith("#")
            output_lines.append(f"<#{i}#> {line}")
        return "\n".join(output_lines)

    @staticmethod
    def escape_braces(text: str) -> str:
        return re.sub(r"([{}])", r"{{\\1}}", text)

    @staticmethod
    def _extract_json(text: str):
        match = re.search(r"{[\s\S]*}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None


# ---------------------------------------------------------------------------
# CLI -----------------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python guardian.py <script-file-or-dir>")

    target = Path(sys.argv[1])
    guardian = MultiChat()

    print("=========== OUTPUT =============\n")
    if target.is_file():
        if target.suffix.lower() not in {".ps1", ".groovy"}:
            sys.exit("ERR: Unsupported script type → " + target.suffix)
        print(f"--- Analyzing: {target.name} ---")
        res = guardian.analyse_file(target)
        print(json.dumps(res, indent=2))
    elif target.is_dir():
        out_xlsx = Path("guardian_batch_report.xlsx")
        guardian.analyse_folder(target, out_xlsx)
        print(f"✅ Batch report saved to: {out_xlsx}")
    else:
        sys.exit("ERR: Not a valid file or directory → " + str(target))


