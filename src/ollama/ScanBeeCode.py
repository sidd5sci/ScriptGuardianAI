# scanBee.py (updated to use two-stage analysis)
from __future__ import annotations
import os, sys, json, re
from pathlib import Path
from typing import List

from langchain_community.chat_models import ChatOllama
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate

# Configurations
CHROMA_DIR   = os.getenv("SECSCAN_DB", "db")
# Use a code-specialized model like "codellama:latest" for better script analysis
LLM_MODEL    = os.getenv("SECSCAN_MODEL", "codellama:latest")
K_SHOT       = int(os.getenv("SECSCAN_KSHOT", "3"))
TEMPERATURE  = float(os.getenv("SECSCAN_T", "0"))

class ScanBee:
    def __init__(self,
                 llm_model: str = LLM_MODEL,
                 k: int = K_SHOT,
                 temperature: float = TEMPERATURE):

        self.llm        = ChatOllama(model=llm_model, temperature=temperature)
        self.parser     = JsonOutputParser()
        self.prompt     = None
        self.prompt_file_path = '/Users/siddhartha.singh/scaningBee/src/ollama/prompts/'

    def _build_messages(self, input_str: str) -> List[dict]:
        safe_input = self.escape_braces(input_str)
        return [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": f"<BEGIN INPUT>\n{safe_input}\n<END INPUT>"}
        ]

    def _to_chat_messages(self, lst):
        role_map = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage}
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    def analyse(self, input_str: str) -> dict:
        raw_messages = self._build_messages(input_str)
        chat_messages = self._to_chat_messages(raw_messages)
        response = self.llm.invoke(chat_messages)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return self._extract_json(response.content) or {"error": "LLM returned invalid JSON", "raw": response.content}

    def analyse_file(self, path: Path, prompt_path: str) -> dict:
        code = path.read_text(encoding="utf-8", errors="ignore")
        code = self.strip_commented_lines(code)
        prompt_path = Path(self.prompt_file_path) / prompt_path
        self.prompt = prompt_path.read_text(encoding="utf-8", errors="ignore")
        return self.analyse(code)

    def analyse_from_json(self, json_obj: dict, prompt_path: str) -> dict:
        prompt_path = Path(self.prompt_file_path) / prompt_path
        self.prompt = prompt_path.read_text(encoding="utf-8", errors="ignore")
        input_str = json.dumps(json_obj, indent=2)
        return self.analyse(input_str)

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

    def strip_commented_lines(self, code: str) -> str:
        return "\n".join(line for line in code.splitlines() if not line.strip().startswith("#"))

if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python scanBee.py <script-file>")

    file_path = Path(sys.argv[1])

    if not file_path.is_file():
        sys.exit(f"ERR: {file_path} not found or not a file")

    bee = ScanBee()

    # First pass: detect sensitive vaiables JSON
    print("\n===========STAGE 1: Detect sensitive================\n")
    sensitive_variable = bee.analyse_file(file_path, "variable/prompt_1.md")
    print(json.dumps(sensitive_variable, indent=2))

    # Second pass: generate summary JSON
    print("\n===========STAGE 2: Static Summary================\n")
    static_summary = bee.analyse_file(file_path, "summary/prompt_6.md")
    print(json.dumps(static_summary, indent=2))

    # Third pass: feed JSON into a vulnerability prompt
    print("\n===========STAGE 3: Vulnerability Detection================\n")
    vuln_analysis = bee.analyse_from_json(static_summary, "analyse/prompt_7.md")
    print(json.dumps(vuln_analysis, indent=2))