# scanBee.py (updated with code-focused model)
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

    def _build_messages(self, code: str) -> List[dict]:
        safe_code = self.escape_braces(code)
        return [
            {"role": "system", "content": self.prompt},
            {"role": "user", "content": f"<BEGIN CODE>\n{safe_code}\n<END CODE>"}
        ]

    def _to_chat_messages(self, lst):
        role_map = {"system": SystemMessage, "user": HumanMessage, "assistant": AIMessage}
        return [role_map[m["role"]](content=m["content"]) for m in lst]

    def analyse(self, code: str) -> dict:
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        response = self.llm.invoke(chat_messages)
        try:
            return json.loads(response.content)
        except json.JSONDecodeError:
            return self._extract_json(response.content) or {"error": "LLM returned invalid JSON", "raw": response.content}

    def analyse_file(self, path: Path, prompt_path: Path) -> dict:
        code = path.read_text(encoding="utf-8", errors="ignore")
        code = self.strip_commented_lines(code)
        self.prompt = prompt_path.read_text(encoding="utf-8", errors="ignore")
        return self.analyse(code)

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
    if len(sys.argv) < 3:
        sys.exit("Usage: python scanBee.py <script-file> <prompt-file>")

    file_path = Path(sys.argv[1])
    prompt_path = Path(sys.argv[2])

    if not file_path.is_file():
        sys.exit(f"ERR: {file_path} not found or not a file")

    bee = ScanBee()
    result = bee.analyse_file(file_path, prompt_path)

    print("===========OUTPUT================\n\n")
    print(json.dumps(result, indent=2))

    result2 = bee.analyse_file(file_path, prompt_path)
