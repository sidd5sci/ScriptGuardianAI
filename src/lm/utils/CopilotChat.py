"""
Thin wrapper for LogicMonitor’s Claude 3 “generate-response” endpoint.

Environment variables
---------------------
CLAUDE_BASE_URL   default: https://lm-copilot-test-us-west-2.logicmonitor.net/llm
CLAUDE_MODEL      default: bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0
CLAUDE_TOP_K      default: 2
"""

from __future__ import annotations

import os
import requests
from typing import List

from langchain_core.messages import BaseMessage, SystemMessage, HumanMessage, AIMessage


class CopilotChat:
    def __init__(
        self,
        model: str | None = None,
        base_url: str | None = None,
        top_k: int | None = None,
        temperature: float = 0.0,
    ):
        self.base_url = (base_url or
                         os.getenv("CLAUDE_BASE_URL",
                                   "https://lm-copilot-test-us-west-2.logicmonitor.net/llm")).rstrip(
            "/")
        self.endpoint = f"{self.base_url}/generate-response"
        self.model = model or os.getenv(
            "CLAUDE_MODEL",
            "bedrock/us.anthropic.claude-3-7-sonnet-20250219-v1:0")
        self.top_k = top_k or int(os.getenv("CLAUDE_TOP_K", "2"))
        self.temperature = temperature
        raw = os.getenv("CLAUDE_VERIFY_SSL", "1").strip().lower()
        if raw in {"0", "false", "no"}:             # ← disable verify
            self.verify_ssl: bool | str = False
        else:                                       # ← default (system CAs)
            self.verify_ssl = True

    # ------------------------------------------------------------------ #
    # Public call
    # ------------------------------------------------------------------ #
    def invoke(self, messages: List[BaseMessage]):
        user_parts = [m.content for m in messages if isinstance(m, HumanMessage)]
        query = user_parts[-1] if user_parts else messages[-1].content

        full_prompt = self._concat_prompt(messages)

        payload = {
            "query": query,
            "prompt": full_prompt,
            "collectionname": "guardian-runtime",
            "similaritysearch": True,
            "top_k": self.top_k,
            "model": self.model,
        }

        headers = {"Content-Type": "application/json", "Accept-Language": "en-US"}

        resp = requests.post(self.endpoint, json=payload, headers=headers, timeout=600, verify=self.verify_ssl)
        resp.raise_for_status()
        text = resp.json()["response"]  # API returns:  {"response": "..."}
        return AIMessage(content=text)

    # ------------------------------------------------------------------ #
    # Helper: merge messages into single Claude prompt template
    # ------------------------------------------------------------------ #
    @staticmethod
    def _concat_prompt(messages: List[BaseMessage]) -> str:
        """
        Turn a message list into:  "System: ...\\nUser: ...\\nAssistant: ..."
        Claude doesn’t need role tokens – we just inline them for context.
        """
        role_map = {
            SystemMessage: "System",
            HumanMessage: "User",
            AIMessage: "Assistant",
        }
        parts = []
        for m in messages:
            role = role_map.get(type(m), "User")
            parts.append(f"{role}: {m.content}")
        return "\n".join(parts)
