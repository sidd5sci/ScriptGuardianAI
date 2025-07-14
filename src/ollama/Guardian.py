"""Guardian security‑scan driver that now uses the local **Ollama** HTTP API
via the `OllamaChat` wrapper (see *ollama_chat.py* in this repo). The rest of
its behaviour remains unchanged.

Usage
-----
$ export SECSCAN_MODEL="gemma:2b"
$ python guardian.py my_script.ps1
"""
from __future__ import annotations

import json
import os
import re
import sys
from pathlib import Path
from typing import List, Dict, Any

import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate  # noqa: F401 (kept for future templating)

# 👉  Our new local‑LLM client
from src.ollama.Ollama import OllamaChat

# ---------------------------------------------------------------------------
# Configuration ----------------------------------------------------------------
# ---------------------------------------------------------------------------
LLM_MODEL = os.getenv("SECSCAN_MODEL", "claude-3.7-sonnet-reasoning-gemma3-12b")
TEMPERATURE = float(os.getenv("SECSCAN_T", "0"))
OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/chat")

# ---------------------------------------------------------------------------
# Guardian ---------------------------------------------------------------------
# ---------------------------------------------------------------------------
class Guardian:
    """Static‑analysis helper that queries an LLM for vulnerabilities."""

    def __init__(self, llm_model: str = LLM_MODEL, temperature: float = TEMPERATURE):
        # Switch from LMStudioChat ➜ OllamaChat
        self.llm = OllamaChat(model=llm_model, temperature=temperature, url=OLLAMA_URL)

        self.parser = JsonOutputParser()
        self.prompt_ps1 = Path("src/lm/prompts/powershell/prompt_11.md")
        self.prompt_groovy = Path("src/lm/prompts/groovy/prompt_9.md")
        self._line_map: Dict[int, bool] = {}

        if not all(p.is_file() for p in (self.prompt_ps1, self.prompt_groovy)):
            sys.exit("ERR: One or more prompt files not found.")

    # ---------------------------------------------------------------------
    # Internal helpers -----------------------------------------------------
    # ---------------------------------------------------------------------
    @staticmethod
    def _to_chat_messages(msg_dicts: List[Dict[str, str]]):
        role_map = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage,
        }
        return [role_map[m["role"]](content=m["content"]) for m in msg_dicts]

    @staticmethod
    def escape_braces(text: str) -> str:
        """Escape braces so they’re not parsed as prompt‑template placeholders."""
        return re.sub(r"([{}])", r"{{\\1}}", text)

    # ---------------------------------------------------------------------
    # Prompt builders ------------------------------------------------------
    # ---------------------------------------------------------------------
    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        return [
            {
                "role": "user",
                "content": f"{self.prompt.strip()}\n\n<BEGIN CODE>\n{safe_code}\n<END CODE>",
            }
        ]

    def with_line_markers(self, code: str) -> str:
        """Prepend `<#n#>` markers so the LLM can quote precise line numbers."""
        self._original_lines = code.splitlines()
        self._line_map = {}
        out: List[str] = []
        for i, line in enumerate(self._original_lines):
            n = i + 1
            is_comment = line.strip().startswith("#")
            self._line_map[n] = is_comment
            out.append(f"<#${n}#> {line}")
        return "\n".join(out)

    # ---------------------------------------------------------------------
    # Core public API ------------------------------------------------------
    # ---------------------------------------------------------------------
    def analyse(self, code: str) -> Dict[str, Any]:
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        response_msg = self.llm.invoke(chat_messages)

        raw_json = self._extract_json(response_msg.content)
        if not raw_json:
            print(" ⚠️  Invalid JSON. Retrying with reformatting prompt …")
            raw_json = self.reformat_invalid_json(response_msg.content)
        if not raw_json:
            return {"error": "LLM returned non‑JSON format twice", "raw": response_msg.content}

        findings = raw_json.get("findings", [])
        clean_findings = []
        for f in findings:
            line_no = f.get("line")
            # If the line is wrapped like <#42#>
            if isinstance(line_no, str) and line_no.startswith("<#") and line_no.endswith("#>"):
                try:
                    line_no = int(line_no[2:-2])
                    f["line"] = line_no
                except ValueError:
                    f["line"] = -1
            if isinstance(line_no, int) and not self._line_map.get(line_no, False):
                clean_findings.append(f)

        score = 10 - sum(1 for f in clean_findings if f.get("severity", "").lower() == "error")
        return {
            "script": "safe" if score == 10 else "vulnerable",
            "score": score,
            "findings": clean_findings,
        }

    # ------------------------------------------------------------------
    # File / folder helpers -------------------------------------------
    # ------------------------------------------------------------------
    def analyse_file(self, path: Path) -> Dict[str, Any]:
        code = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix.lower() == ".ps1":
            self.prompt = self.prompt_ps1.read_text(encoding="utf-8", errors="ignore")
        elif path.suffix.lower() == ".groovy":
            self.prompt = self.prompt_groovy.read_text(encoding="utf-8", errors="ignore")
        else:
            raise ValueError("Unsupported file extension: " + path.suffix)

        instrumented = self.with_line_markers(code)
        return self.analyse(instrumented)

    def analyse_folder(self, folder: Path, output_excel: Path):
        rows = []
        print("Analyzing folder:", folder)

        for file in sorted(folder.glob("*")):
            if file.suffix.lower() not in {".ps1", ".groovy", ".txt"}:
                continue

            print(f"\n--- Analyzing: {file.name} ---")
            try:
                result = self.analyse_file(file)
                output = json.dumps(result, indent=2)
                status = result.get("script", "error")
            except Exception as e:
                output = f"ERROR: {e}"
                status = "error"

            rows.append(
                {
                    "script": file.read_text(encoding="utf-8", errors="ignore"),
                    "output": output,
                    "vulnerable/safe": status,
                    "expected": "",
                }
            )

        pd.DataFrame(rows).to_excel(output_excel, index=False)
        return output_excel

    # ------------------------------------------------------------------
    # JSON helpers ------------------------------------------------------
    # ------------------------------------------------------------------
    @staticmethod
    def _extract_json(text: str):
        match = re.search(r"\{[\s\S]*\}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None

    def reformat_invalid_json(self, malformed: str):
        retry_prompt = (
            "You are a JSON validation assistant. The next input is supposed to be a valid "
            "JSON object, but it may include markdown formatting or commentary. "
            "Return **ONLY** the corrected JSON object—no explanation, no code fences."
        )
        retry_messages = [
            {"role": "user", "content": retry_prompt + "\n\n" + malformed.strip()}
        ]
        chat_msgs = self._to_chat_messages(retry_messages)
        retry_resp = self.llm.invoke(chat_msgs)
        return self._extract_json(retry_resp.content)


# ---------------------------------------------------------------------------
# CLI -----------------------------------------------------------------------
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python guardian.py <script-file-or-dir>")

    target = Path(sys.argv[1])
    guardian = Guardian()

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
