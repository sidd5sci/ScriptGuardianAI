"""Compose chat messages with k‑shot few‑shot examples."""
from textwrap import indent
from typing import Dict, List
from .retriever import k_shot
from .config import SENSITIVE_KEY_RE

_PROMPT = """
Analyse the following PowerShell or Groovy code.
1. Identify variables that store **sensitive host properties** (keys =~ /{regex}/).
2. For each, list operations that could leak it (console, file, network, copy).
Return strict JSON:
{{
  "findings":[
    {{
      "var":"<name>",
      "reason":"<why sensitive>",
      "leaks":[{{"sink":"<op>","line":<int>,"explanation":"<text>"}}]
    }}
  ]
}}

SYMBOL TABLE:
{symbols}

<BEGIN CODE>
{code}
<END CODE>
""".strip()

def build_messages(chunk: Dict, k: int = 3) -> List[Dict[str,str]]:
    symbols = "\n".join(f"• {n} @+{ln}" for n, ln in chunk["vars"]) or "(none)"
    user_prompt = _PROMPT.format(regex=SENSITIVE_KEY_RE, symbols=symbols, code=indent(chunk["code"], "  "))
    msgs = [{"role":"system","content":"You are SecScan‑GPT running fully offline."}]
    for up, ac in k_shot(user_prompt, k):
        msgs.append({"role":"user","content":up})
        msgs.append({"role":"assistant","content":ac})
    msgs.append({"role":"user","content":user_prompt})
    return msgs
