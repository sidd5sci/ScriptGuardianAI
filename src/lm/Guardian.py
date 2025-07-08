from __future__ import annotations
import os, sys, json, re
import requests
from pathlib import Path
from typing import List
import pandas as pd
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate
from src.lm.LMStudio import LMStudioChat


LLM_MODEL = os.getenv("SECSCAN_MODEL", "claude-3.7-sonnet-reasoning-gemma3-12b")
TEMPERATURE = float(os.getenv("SECSCAN_T", "0"))

class Guardian:
    def __init__(self, llm_model: str = LLM_MODEL, temperature: float = TEMPERATURE):
        self.llm = LMStudioChat(model=llm_model, temperature=temperature)
        self.parser = JsonOutputParser()
        self.prompt = None
        self._line_map = {}

    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        return [{
            "role": "user",
            "content": f"{self.prompt.strip()}\n\n<BEGIN CODE>\n{safe_code}\n<END CODE>"
        }]

    def _to_chat_messages(self, lst):
        role_map = {"user": HumanMessage, "assistant": AIMessage}
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    def analyse(self, code: str) -> dict:
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        response = self.llm.invoke(chat_messages)

        raw_json = self._extract_json(response.content)
        if not raw_json:
            return {"error": "LLM returned invalid JSON", "raw": response.content}

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
        return {
            "script": "safe" if score == 10 else "vulnerable",
            "score": score,
            "findings": clean_findings
        }

    def analyse_file(self, path: Path, prompt_path: Path) -> dict:
        code = path.read_text(encoding="utf-8", errors="ignore")
        self.prompt = prompt_path.read_text(encoding="utf-8", errors="ignore")
        instrumented_code = self.with_line_markers(code)
        return self.analyse(instrumented_code)

    def analyse_folder(self, folder: Path, prompt_ps1: Path, prompt_groovy: Path, output_excel: Path):
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

    def _extract_json(self, text: str) -> dict | None:
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                return json.loads(match.group(0))
        except Exception:
            pass
        return None

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python Guardian.py <script-file-or-dir>")

    input_path = Path(sys.argv[1])
    prompt_ps1 = Path("src/lm/prompts/powershell/prompt_10.md")
    prompt_groovy = Path("src/lm/prompts/groovy/prompt_9.md")

    if not all(p.is_file() for p in [prompt_ps1, prompt_groovy]):
        sys.exit("ERR: One or more prompt files not found.")

    bee = Guardian()
    print("===========OUTPUT=================\n")

    if input_path.is_file():
        if input_path.suffix.lower() not in {".ps1", ".groovy", ".txt"}:
            sys.exit(f"ERR: {input_path} is not a supported script file")
        print(f"--- Analyzing: {input_path.name} ---")
        result = bee.analyse_file(input_path, prompt_ps1)
        print(json.dumps(result, indent=2))

    elif input_path.is_dir():
        excel_output = Path("guardian_batch_report.xlsx")
        output_file = bee.analyse_folder(input_path, prompt_ps1, prompt_groovy, excel_output)
        print(f"✅ Batch report saved to: {output_file}")

    else:
        sys.exit(f"ERR: {input_path} is not a valid file or directory")