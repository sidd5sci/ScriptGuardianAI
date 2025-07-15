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

LLM_MODEL_OLLAMA = os.getenv("SECSCAN_MODEL", "hf.co/reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled:latest")
LLM_MODEL = os.getenv("SECSCAN_MODEL", "claude-3.7-sonnet-reasoning-gemma3-12b")
TEMPERATURE = float(os.getenv("SECSCAN_T", "0.1"))
PLATFORM = os.getenc("PLATFORM", "lmstudio") # ollama, lmstudio

class Guardian:
    def __init__(self, llm_model: str = LLM_MODEL, temperature: float = TEMPERATURE):
        
        self.llm = LMStudioChat(model=llm_model, temperature=temperature)
        self.parser = JsonOutputParser()
        self.prompt_ps1 = Path("src/lm/prompts/powershell/prompt_11.md")
        self.prompt_groovy = Path("src/lm/prompts/groovy/prompt_9.md")
        self._line_map = {}
        
        if not all(p.is_file() for p in [self.prompt_ps1, self.prompt_groovy]):
            sys.exit("ERR: One or more prompt files not found.")

    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        return [{
            "role": "user",
            "content": f"{self.prompt.strip()}\n\n<BEGIN CODE>\n{safe_code}\n<END CODE>"
        }]

    def _to_chat_messages(self, lst):
        role_map = {
            "system": SystemMessage,
            "user": HumanMessage,
            "assistant": AIMessage
        }
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    def analyse(self, code: str) -> dict:
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        response = self.llm.invoke(chat_messages)

        raw_json = self._extract_json(response.content)

        if not raw_json:
            print(" ⚠️ Invalid JSON. Retrying with reformatting prompt...")
            raw_json = self.reformat_invalid_json(response.content)
        
        if not raw_json:
            return {"error": "LLM returned non-JSON format twice", "raw": raw_json}

        # print("DEBUG Response:", raw_json, type(raw_json))
        

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

    def analyse_file(self, path: Path, file_extension: str) -> dict: 
        code = path.read_text(encoding="utf-8", errors="ignore")
        if file_extension == ".ps1":
            self.prompt = self.prompt_ps1.read_text(encoding="utf-8", errors="ignore")
        elif file_extension == ".groovy":
            self.prompt = self.prompt_groovy.read_text(encoding="utf-8", errors="ignore")

        instrumented_code = self.with_line_markers(code)
        return self.analyse(instrumented_code)

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



if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python Guardian.py <script-file-or-dir>")

    input_path = Path(sys.argv[1])
    bee = Guardian()
    print("===========OUTPUT=================\n")

    if input_path.is_file():
        if input_path.suffix.lower() not in {".ps1", ".groovy"}:
            sys.exit(f"ERR: {input_path} is not a supported script file")
        print(f"--- Analyzing: {input_path.name} ---")
        result = bee.analyse_file(input_path, input_path.suffix.lower())
        print(json.dumps(result, indent=2))

    elif input_path.is_dir():
        excel_output = Path("guardian_batch_report.xlsx")
        output_file = bee.analyse_folder(input_path, excel_output)
        print(f"✅ Batch report saved to: {output_file}")

    else:
        sys.exit(f"ERR: {input_path} is not a valid file or directory")