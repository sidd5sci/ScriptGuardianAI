# scanBee.py (updated)
from __future__ import annotations
import os, sys, json, re
from pathlib import Path
from typing import List

from langchain_community.embeddings import OllamaEmbeddings
from langchain_community.chat_models import ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import JsonOutputParser
from langchain.prompts import ChatPromptTemplate

# Configurations
CHROMA_DIR   = os.getenv("SECSCAN_DB", "db")
EMB_MODEL    = os.getenv("SECSCAN_EMB_MODEL", "nomic-embed-text")
LLM_MODEL    = os.getenv("SECSCAN_MODEL", "llama3")
K_SHOT       = int(os.getenv("SECSCAN_KSHOT", "3"))
TEMPERATURE  = float(os.getenv("SECSCAN_T", "0"))

class ScanBee:
    def __init__(self,
                 chroma_dir: str = CHROMA_DIR,
                 emb_model: str = EMB_MODEL,
                 llm_model: str = LLM_MODEL,
                 k: int = K_SHOT,
                 temperature: float = TEMPERATURE):

        self.embeddings = OllamaEmbeddings(model=emb_model, show_progress=True)
        self.db         = Chroma(persist_directory=chroma_dir,
                                 embedding_function=self.embeddings)
        self.retriever  = self.db.as_retriever(search_kwargs={"k": k})
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