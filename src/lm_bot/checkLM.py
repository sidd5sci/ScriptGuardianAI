from __future__ import annotations
import os, sys, json, re
import requests
from pathlib import Path
from typing import List

#from langchain_ollama import ChatOllama
#from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate

LLM_MODEL    = os.getenv("SECSCAN_MODEL", "claude-3.7-sonnet-reasoning-gemma3-12b")
TEMPERATURE  = float(os.getenv("SECSCAN_T", "0"))

class LMStudioChat:
    def __init__(self, model: str, temperature: float = 0.0, url: str = "http://127.0.0.1:1234/v1/chat/completions"):
        self.model = model
        self.temperature = temperature
        self.url = url
        self.repetition_penalty = 1.15
        self.top_p = 0.9


    def invoke(self, messages):
        openai_messages = []
        for m in messages:
            if isinstance(m, SystemMessage):
                role = "system"
            elif isinstance(m, HumanMessage):
                role = "user"
            elif isinstance(m, AIMessage):
                role = "assistant"
            else:
                raise ValueError(f"Unsupported message type: {type(m)}")
            openai_messages.append({"role": role, "content": m.content})

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
            "stream": False
        }

        # print("DEBUG Payload:", json.dumps(payload, indent=2))

        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            print("LM Studio error response:")
            print(response.text)
        response.raise_for_status()

        result = response.json()
        return AIMessage(content=result["choices"][0]["message"]["content"])

class ScanBee:
    def __init__(self,
                 llm_model: str = LLM_MODEL,
                 temperature: float = TEMPERATURE):

        self.llm    = LMStudioChat(model=llm_model, temperature=temperature)
        self.parser = JsonOutputParser()
        self.prompt = None
        self._line_map = {}

    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        # Inline the system instructions into the user message
        return [
            {
                "role": "user",
                "content": f"{self.prompt.strip()}\n\n<BEGIN CODE>\n{safe_code}\n<END CODE>"
            }
        ]

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

    def with_line_markers(self, code: str) -> str:
        self._original_lines = code.splitlines()
        self._line_map = {}  # line_num: is_comment

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
        sys.exit("Usage: python scanBee.py <script-file-or-dir> <prompt-file>")

    input_path = Path(sys.argv[1])
    prompt_path = Path("src/ollama/prompts/powershell/prompt_10.md")

    if not prompt_path.is_file():
        sys.exit(f"ERR: {prompt_path} not found or not a file")

    bee = ScanBee()
    print("===========OUTPUT=================\n\n")

    if input_path.is_file():
        if input_path.suffix.lower() not in {".ps1", ".groovy", ".txt"}:
            sys.exit(f"ERR: {input_path} is not a supported script file")
        
        print(f"\n--- Analyzing: {input_path.name} ---\n")
        result = bee.analyse_file(input_path, prompt_path)
        print(json.dumps(result, indent=2))

    elif input_path.is_dir():
        for script_file in sorted(input_path.glob("*")):
            if script_file.suffix.lower() not in {".ps1", ".groovy", ".txt"}:
                continue  # skip non-script files

            print(f"\n--- Analyzing: {script_file.name} ---\n")
            result = bee.analyse_file(script_file, prompt_path)
            print(json.dumps(result, indent=2))

    else:
        sys.exit(f"ERR: {input_path} is not a valid file or directory")

