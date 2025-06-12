"""
scanBee – local RAG bot for script-security scanning
===================================================

Usage
-----
python scanBee.py path/to/script.ps1

• Reads the script, embeds & retrieves k-nearest labelled examples from Chroma
• Feeds examples + target script to a local LLM (Ollama / llama.cpp or HF)
• Prints JSON findings (var, leak type, reason, etc.)
"""

from __future__ import annotations
import os, sys, json, re
from pathlib import Path
from typing import List

# -- LangChain community connectors
# from langchain_community.vectorstores import Chroma
from langchain_community.embeddings import OllamaEmbeddings   # swap if you prefer HF
from langchain_community.chat_models import ChatOllama
# from langchain_ollama import OllamaEmbeddings, ChatOllama
from langchain_chroma import Chroma
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage
from langchain_core.output_parsers import StrOutputParser
from langchain.prompts import ChatPromptTemplate

# ---------------- configuration -----------------
CHROMA_DIR   = os.getenv("SECSCAN_DB", "db")
EMB_MODEL    = os.getenv("SECSCAN_EMB_MODEL", "nomic-embed-text")
LLM_MODEL    = os.getenv("SECSCAN_MODEL", "llama3")   # any Ollama tag
K_SHOT       = int(os.getenv("SECSCAN_KSHOT", "3"))
TEMPERATURE  = float(os.getenv("SECSCAN_T", "0"))
# ------------------------------------------------

class ScanBee:
    """RAG-powered script-security assistant."""

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
        self.parser     = StrOutputParser()
        self.prompt = None

    # ---------- prompt helpers ----------
    def _example_to_messages(self, doc) -> List[dict]:
        code      = doc.page_content
        meta      = doc.metadata
        finding   = meta.get("completion")  # stored JSON
        if not finding:
            finding = '{"findings": []}'

        # ➜ Escape curly braces so LangChain won't think
        #   they are template variables.
        code    = self.escape_braces(code)
        finding = self.escape_braces(finding)

        return [
            {"role": "user",      "content": f"<BEGIN CODE>\n{code}\n<END CODE>"},
            {"role": "assistant", "content": finding},
        ]

    def _doc_to_msgs(doc):
        code = escape_braces(doc.page_content)
        # assistant message now holds *only* the verdict JSON you stored
        gold = doc.metadata.get("completion", '{"script":"benign","findings":[]}')

        return [
            HumanMessage(content=f"<BEGIN CODE>\n{code}\n<END CODE>"),
            AIMessage(content=gold),
        ]

    def _build_messages(self, code: str) -> List[dict]:
        """Assemble system + few-shot + target user messages."""
        messages: List[dict] = [
                {
                "role": "system",
                "content": self.prompt
            }
        ]

         # target script (escape braces)
        safe_code = self.escape_braces(code)
        messages.append({
            "role": "user",
            "content": (f"<BEGIN CODE>\n{safe_code}\n<END CODE>")
            })
        return messages
    # ------------------------------------
    def _to_chat_messages(self, lst):
        out = []
        for m in lst:
            role = m["role"]
            cls  = {"system": SystemMessage,
                    "user":   HumanMessage,
                    "assistant": AIMessage}[role]
            out.append(cls(content=m["content"]))
        return out

    def analyse(self, code: str) -> str:
        """Return JSON string with findings."""
        raw_messages = self._build_messages(code)
        chat_messages = self._to_chat_messages(raw_messages)
        # prompt = ChatPromptTemplate.from_messages(msgs)
        response = self.llm.invoke(chat_messages)   # ChatOllama returns a Message
        return response.content                     # plain string (JSON)
        # json_str = (prompt | self.llm | self.parser).invoke({})
        # return json_str

    def analyse_file(self, path: Path, prompt_path: Path) -> dict:
        code = path.read_text(encoding="utf-8", errors="ignore")
        self.prompt = prompt_path.read_text(encoding="utf-8", errors="ignore")
        raw  = self.analyse(code)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            fixed = self._extract_json(raw)
            if fixed:
                return fixed
            return {"error": "LLM returned invalid JSON", "raw": raw}

    def escape_braces(self, text: str) -> str:
        # replace { with {{ and } with }}
        return re.sub(r"([{}])", r"{{\1}}", text)

    def _extract_json(self, text: str) -> dict | None:
        """Extract and parse the first JSON object from raw text."""
        try:
            match = re.search(r'\{.*\}', text, re.DOTALL)
            if match:
                json_str = match.group(0)
                return json.loads(json_str)
        except Exception:
            pass
        return None
# ---------------- CLI runner --------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python scanBee.py <script-file>")

    file_path = Path(sys.argv[1])
    prompt = Path(sys.argv[2])
    if not file_path.is_file():
        sys.exit(f"ERR: {file_path} not found or not a file")

    bee = ScanBee()
    result = bee.analyse_file(file_path, prompt)
    print("===========OUTPUT================\n\n")
    print(json.dumps(result, indent=2))
