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

python -m src.lm.Guardian tests/powershell/batch1/script_01.ps1
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
from src.lm.utils.Ollama import OllamaChat
from src.lm.utils.LMStudio import LMStudioChat
from src.lm.utils.validator import ScriptFindingValidator as VF
import replicate

# ---------------------------------------------------------------------------
# Back‑end & model configuration
# ---------------------------------------------------------------------------
BACKEND = os.getenv("LLM_BACKEND", "lmstudio").lower()  # "ollama" | "lmstudio"

DEFAULT_OLLAMA_MODEL = "hf.co/reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled:latest"
DEFAULT_LMS_MODEL = "claude-3.7-sonnet-reasoning-gemma3-12b"

OLLAMA_MODEL = os.getenv("SECSCAN_MODEL_OLLAMA", DEFAULT_OLLAMA_MODEL)
LMS_MODEL = os.getenv("SECSCAN_MODEL_LMS", DEFAULT_LMS_MODEL)

TEMPERATURE = float(os.getenv("SECSCAN_T", "0"))


class Guardian:
    """Analyse PowerShell & Groovy scripts for security issues using an LLM."""

    def __init__(self, backend: str = BACKEND, temperature: float = TEMPERATURE):
        self.backend = backend
        self.temperature = temperature
        self.prompt = None

        if backend == "ollama":
            self.llm = OllamaChat(model=OLLAMA_MODEL, temperature=temperature)
        elif backend == "lmstudio":
            self.llm = LMStudioChat(model=LMS_MODEL, temperature=temperature)
        else:
            raise ValueError("backend must be 'ollama' or 'lmstudio'")

        # --- parser & prompt paths ---
        self.prompt_ps1 = Path("src/lm/prompts/powershell/prompt_13.md")
        self.prompt_groovy = Path("src/lm/prompts/groovy/prompt_9.md")

        if not (self.prompt_ps1.is_file() and self.prompt_groovy.is_file()):
            sys.exit("ERR: prompt files missing")

        self._line_map: Dict[int, bool] = {}

    # ------------------------------ chat glue -----------------------------
    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        return [{
            "role": "user",
            "content": f"{self.prompt.strip()}\n\n<BEGIN CODE>\n{safe_code}\n<END CODE>"
        }]

    # ------------------------------ chat glue -----------------------------
    def _to_chat_messages(self, lst):
        role_map = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage
        }
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    # ------------------------------ analysis -----------------------------
    def analyse(self, code: str) -> dict:
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        response = self.llm.invoke(chat_messages)

        raw_json = self._extract_json(response.content)

        if not raw_json:
            print(" ⚠️ Invalid JSON. Retrying with reformatting prompt...")
            #raw_json = self.reformat_invalid_json(response.content)

        # if not raw_json:
        #     return {"error": "LLM returned non-JSON format twice", "raw": raw_json}

        # print("DEBUG Response:", raw_json, type(raw_json))
        print("DEBUG Response:",response.content)

        findings = raw_json.get("findings", [])
        clean_findings = []

        for f in findings:
            line_no = f.get("line")
            if isinstance(line_no, str) and line_no.startswith("<#") and line_no.endswith("#>"):
                try:
                    line_no = int(line_no[2:-2])
                    f["line"] = line_no
                except ValueError:
                    f["line"] = -1
            if isinstance(line_no, int) and not self._line_map.get(line_no, False):
                clean_findings.append(f)

        score = 10 - sum(1 for f in clean_findings if f["severity"].lower() == "error")
        response = {
            "script": "safe" if score == 10 else "vulnerable",
            "score": score,
            "findings": clean_findings
        }

        diffs = VF.validate_from_strings(code, response)
        if diffs:
            print("⚠️  mismatches -> trying realign")
            response = VF.realign_findings(code, response)

        # You can validate again or just print
        # print("Validation (after realign):", VF.validate_from_strings(code, response))
        
        return response
    # ------------------------- analyse file ----------------------
    def analyse_code(self, code: str, scriptType: str) -> Dict[str, Any]:
        
        if scriptType.lower() == "powershell":
            self.prompt = self.prompt_ps1.read_text(encoding="utf-8", errors="ignore")
        elif scriptType.lower() == "groovy":
            self.prompt = self.prompt_groovy.read_text(encoding="utf-8", errors="ignore")
        else:
            raise ValueError("Unsupported file type")
        print(scriptType)
        instrumented_code = self.with_line_markers(code)
        return self.analyse(instrumented_code)

    # ------------------------- analyse file ----------------------
    def analyse_file(self, path: Path) -> Dict[str, Any]:
        code = path.read_text(encoding="utf-8", errors="ignore")
        if path.suffix.lower() == ".ps1":
            self.prompt = self.prompt_ps1.read_text(encoding="utf-8", errors="ignore")
        elif path.suffix.lower() == ".groovy":
            self.prompt = self.prompt_groovy.read_text(encoding="utf-8", errors="ignore")
        else:
            raise ValueError("Unsupported file type")

        instrumented_code = self.with_line_markers(code)
        return self.analyse(instrumented_code)

    # ------------------------- analyse files in the folder ----------------------
    def analyse_folder(self, folder: Path, output_excel: Path):
        rows = []
        print("Analyzing folder:", folder)

        for file in sorted(folder.glob("*")):
            if file.suffix.lower() not in {".ps1", ".groovy", ".txt"}:
                continue

            # Select appropriate prompt
            prompt = prompt_ps1
            if file.suffix.lower() == ".groovy":
                prompt = prompt_groovy
            
            print("\nPrompt selected:", prompt)
            print(f"--- Analyzing: {file.name} ---")
            try:
                result = self.analyse_file(file, prompt)
                output = json.dumps(result, indent=2)
                print(output)
                status = result.get("script", "error")
            except Exception as e:
                output = f"ERROR: {e}"
                status = "error"

            rows.append({
                "script": file.read_text(encoding="utf-8", errors="ignore"),
                "output": output,
                "vulnerable/safe": status,
                "expected": ""
            })

        pd.DataFrame(rows).to_excel(output_excel, index=False)
        return output_excel.name

    # ----------------------------- utilities -----------------------------
    def with_line_markers(self, code: str) -> str:
        self._original_lines = code.splitlines()
        self._line_map = {}
        output_lines = []
        for i, line in enumerate(self._original_lines):
            line_num = i + 1
            is_comment = line.strip().startswith("#")
            self._line_map[line_num] = is_comment
            output_lines.append(f"<#{line_num}#> {line}")
        return "\n".join(output_lines)

    def escape_braces(self, text: str) -> str:
        return re.sub(r"([{}])", r"{{\\1}}", text)

    def _extract_json(self, text: str):
        match = re.search(r"{[\s\S]*}", text)
        if match:
            try:
                return json.loads(match.group(0))
            except json.JSONDecodeError:
                return None
        return None

    def reformat_invalid_json(self, malformed_text: str) -> dict | None:
        retry_prompt = (
            "You are a JSON validation assistant. The next input is supposed to be a valid JSON object, "
            "but it may include markdown formatting or additional commentary. "
            "Return ONLY the corrected JSON object. "
            "DO NOT include explanations, analysis, prose, code blocks, or anything else. "
            "Your output MUST begin with '{' and end with '}'."
        )
        retry_messages = [
            {"role": "user", "content": retry_prompt+"\n\n"+malformed_text.strip()}
        ]
        chat_messages = self._to_chat_messages(retry_messages)
        retry_response = self.llm.invoke(chat_messages)
        # print("Reformated response:\n", retry_response.content, type(retry_response),"\n")

        try:
            # Step 1: Remove ```json or ``` wrappers if present
            cleaned = retry_response.content.strip()
            cleaned = re.sub(r"^```(?:json)?\s*", "", cleaned, flags=re.IGNORECASE | re.MULTILINE)
            cleaned = re.sub(r"\s*```$", "", cleaned, flags=re.MULTILINE)
            
            # Step 2: Extract JSON block (just in case)
            match = re.search(r'{[\s\S]*}', cleaned)
            if not match:
                print(" No JSON block found in response")
                return None

            json_str = match.group(0)
            # Step 3: Escape invalid backslashes
            json_str = re.sub(r'(?<!\\)\\(?![\\/"bfnrtu])', r'\\\\', json_str)
            # Step 4: Parse to dict
            return json.loads(json_str)

        except Exception as e:
            print(f" Failed to parse JSON: {e}")
        
        return None



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


