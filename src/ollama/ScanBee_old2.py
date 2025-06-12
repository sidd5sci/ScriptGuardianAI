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
from utils.scanflow import quick_flow_scan

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
        static = quick_flow_scan(code)           # DO NOT wrap in print()
        sens_vars = ", ".join(sorted(static["sens_vars"])) or "none"
        
        shots = self.retriever.invoke(code)
        # messages: List[dict] = [
        #         {
        #             "role": "system",
        #             "sensitive_variable_list": sens_vars,
        #             "content": (
        #                 "You are **ScanBee**, an expert PowerShell/Groovy security auditor.\n\n"
        #                 "## Sensitive-property detection rules\n"
        #                 "A variable is considered SENSITIVE if its value matches either of these:\n"
        #                 "  • Regex 1 (full placeholder):\n"
        #                 "    /^((snmp|([0-9]+\\.)?snmptrap)\\.(community|privtoken|authtoken))$"
        #                 "|.*credential$|.*password$|(\\S+((\\.pass)|(\\.auth)|(\\.key)))$"
        #                 "|(aws\\.accesskey)$|(azure\\.secretkey)$|(saas\\.(privatekey|secretkey))$"
        #                 "|(gcp\\.serviceaccountkey)$|(collector\\.sqs\\.(awsaccesskey|awssecretkey))$"
        #                 "|(gcccli.accesskey)$/i\n"
        #                 "  • Regex 2 (SNMP auth): /^(snmp|([0-9]+\\.)?snmptrap)\\.auth$/i\n\n"
        #                 "## What to FLAG\n"
        #                 "Flag ONLY operations where a **sensitive variable** is passed to a leak sink:\n"
        #                 "  • Write-Host / Write-Output  (console)\n"
        #                 "  • Set-Content / Out-File     (file)\n"
        #                 "  • Invoke-RestMethod / Invoke-WebRequest (network)\n"
        #                 "Assignments or copies *without* a sink are NOT suspicious.\n\n"
        #                 "## Response format (STRICT JSON):\n"
        #                 "{\n"
        #                 '  "script": "benign | suspicious",\n'
        #                 '  "findings": [\n'
        #                 '     {"line": <int>, "statement": "<trimmed code>", "reason": "<why>"}\n'
        #                 '  ]\n'
        #                 "}"
        #             )
        #         }
        # ]

        messages: List[dict] = [
            {
                "role": "system",
                "sensitive_variable_list": sens_vars,
                "content": (
                    "You are **ScanBee**, a veteran security auditor specializing in PowerShell and Groovy scripts.\n\n"
                    "## 🎯 Objective\n"
                    "Perform a **sensitive variable leak audit**. Identify where sensitive variables are exposed to high-risk operations (a.k.a. 'leak sinks') such as console output, network transmissions, filesystem writes, environment propagation, or reflective inspection.\n\n"
                    "## 🔐 Sensitive-variable detection rules\n"
                    "A variable is **SENSITIVE** if its name or use matches one of the following patterns:\n"
                    "- **Regex 1 (placeholder-sensitive):**\n"
                    "  /^((snmp|([0-9]+\\.)?snmptrap)\\.(community|privtoken|authtoken))$"
                    "|.*credential$|.*password$|(\\S+((\\.pass)|(\\.auth)|(\\.key)))$"
                    "|(aws\\.accesskey)$|(azure\\.secretkey)$|(saas\\.(privatekey|secretkey))$"
                    "|(gcp\\.serviceaccountkey)$|(collector\\.sqs\\.(awsaccesskey|awssecretkey))$"
                    "|(gcccli.accesskey)$/i\n"
                    "- **Regex 2 (SNMP auth):**\n"
                    "  /^(snmp|([0-9]+\\.)?snmptrap)\\.auth$/i\n\n"
                    "## 🚨 What to FLAG\n"
                    "Flag only those operations where a **sensitive variable** is passed into any of the following sinks (risk surfaces):\n\n"
                    "### Console / Stdout\n"
                    "- Write-Host, Write-Output, println, System.out.print\n\n"
                    "### File System & Serialization\n"
                    "- Set-Content, Out-File, new File().write(), serialize(), ObjectOutputStream\n\n"
                    "### Temporary Files\n"
                    "- Any write to /tmp/, TempFile.create(), or OS-specific temp paths\n\n"
                    "### Logs\n"
                    "- log.info(), log.debug(), logger.write(), or equivalent loggers\n\n"
                    "### Network / HTTP\n"
                    "- Invoke-RestMethod, Invoke-WebRequest, HTTPBuilder.post(), HttpURLConnection\n\n"
                    "### Environment Variables\n"
                    "- [System.Environment]::SetEnvironmentVariable(), System.getenv().put()\n\n"
                    "### Process Arguments / Command-Line\n"
                    "- Start-Process -ArgumentList, Runtime.exec(args), ProcessBuilder(args)\n\n"
                    "### Clipboard / UI Exposure\n"
                    "- Clipboard.setContent(), TextField.setText(), echo in dialogs\n\n"
                    "### Shell Injection / Expansion\n"
                    "- Using backticks or shell eval: `cmd`, sh -c, Runtime.exec()\n\n"
                    "### Exported Modules / Functions\n"
                    "- Any `export`, `public`, or shared module exposing the variable\n\n"
                    "### Reflection / Introspection Tools\n"
                    "- Class.getDeclaredFields(), .metaClass, reflection-based dumps\n\n"
                    "### Remote Session Output\n"
                    "- SSH session echo, Invoke-Command -ScriptBlock {}, remote execution logs\n\n"
                    "### Version Control\n"
                    "- git add/commit showing sensitive variable diffs, tracked by VCS\n\n"
                    "### Crash Dumps / Core Files\n"
                    "- Inclusion in caught exceptions, dumped memory objects\n\n"
                    "## 🚫 Do NOT FLAG\n"
                    "- Assignments, internal variable copies, function arguments not reaching a sink\n"
                    "- Control flows or branches without output/IO interaction\n\n"
                    "## ✅ Response Format (STRICT JSON ONLY):\n"
                    "{\n"
                    "  \"script\": \"benign\" | \"suspicious\",\n"
                    "  \"findings\": [\n"
                    "    {\n"
                    "      \"line\": <int>,\n"
                    "      \"statement\": \"<trimmed code line>\",\n"
                    "      \"reason\": \"<why it's flagged: variable + sink>\"\n"
                    "    }\n"
                    "  ]\n"
                    "}\n"
                    "Ensure correctness, no hallucinations, and no extra text outside the JSON.\n"
                )
            }
        ]

        # for doc in shots:
        #     messages.extend(self._example_to_messages(doc))

        # target script (escape braces)
        safe_code = self.escape_braces(code)

        # target
        print(f"Sensitive variables: {sens_vars}")


        messages.append({
            "role": "user",
            "content": (
                "Below are the list of sensitive vaiables ONLY check these vaiables for leak sink\n"
                f"SENSITIVE VARIABLES: {sens_vars or 'none'}\n\n"
                "Analyse each line and output findings ONLY for real leaks.\n"
                "Once output is ready re-check the ouput and validate it it caontains ONLY sugestive vaiables"
                "Respond in **STRICT JSON** exactly matching the schema given above.\n"
                f"<BEGIN CODE>\n{safe_code}\n<END CODE>"
                
            )
        })

        # messages.append({
        #     "role": "user",
        #     "content": (
        #         "Below are the ONLY lines that contain BOTH a leak-sink command and at "
        #         "least one sensitive variable.\n"
        #         f"SENSITIVE VARIABLES: {sens_vars or 'none'}\n\n"
        #         "👉 **For EACH candidate line** decide:\n"
        #         "   • Is the variable truly sensitive? (use the regex rules.)\n"
        #         "   • Does the line leak the value?\n"
        #         "If YES, add an entry to **findings**.  If NO, skip that line.\n"
        #         "Return ALL findings in STRICT JSON — do **not** omit valid leaks and "
        #         "do not add commentary.\n\n"
        #     )
        # })

        # messages.append({"role": "user", "content": f"<BEGIN CODE>\n{safe_code}\n<END CODE>"})
        # print(messages)
        return messages
   
    
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

    def analyse_file(self, path: Path) -> dict:
        code = path.read_text(encoding="utf-8", errors="ignore")
        raw  = self.analyse(code)
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
            return {"error": "LLM returned invalid JSON", "raw": raw}

    def escape_braces(self, text: str) -> str:
        # replace { with {{ and } with }}
        return re.sub(r"([{}])", r"{{\1}}", text)

# ---------------- CLI runner --------------------
if __name__ == "__main__":
    if len(sys.argv) < 2:
        sys.exit("Usage: python scanBee.py <script-file>")

    file_path = Path(sys.argv[1])
    if not file_path.is_file():
        sys.exit(f"ERR: {file_path} not found or not a file")

    bee = ScanBee()
    result = bee.analyse_file(file_path)

    print(json.dumps(result, indent=2))
