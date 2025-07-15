"""A thin Ollama chat wrapper compatible with LangChain‑style messages.

Supports **both** endpoints:
1. `/api/chat` (Ollama ≥ 0.1.32, OpenAI‑format messages)
2. `/api/generate` (older builds, single‑prompt format)

If `/api/chat` returns *404* or *405* the wrapper automatically
falls back to `/api/generate`.

Example
-------
>>> from langchain_core.messages import SystemMessage, HumanMessage
>>> chat = OllamaChat(model="hf.co/reedmayhew/gemma3-12B-claude-3.7-sonnet-reasoning-distilled:latest")
>>> reply = chat.invoke([
...     SystemMessage(content="You are a helpful assistant."),
...     HumanMessage(content="Hello, what's 2+2?")
... ])
>>> print(reply.content)
'4'
"""
from __future__ import annotations

import json
from typing import List, Dict
import requests,os
from langchain_core.messages import (
    SystemMessage,
    HumanMessage,
    AIMessage,
    BaseMessage,
)

__all__ = ["OllamaChat"]


class OllamaChat:  # pylint: disable=too-few-public-methods
    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        host: str = "http://localhost:11434",
        timeout: int | float = 2000,
        top_p: float = 0.9,
        force_generate: bool = True,
    ) -> None:
        self.model = model
        self.temperature = float(temperature)
        self.top_p = top_p
        self.timeout = timeout
        self.base = host.rstrip("/")
        self._chat_url = f"{self.base}/api/chat"
        self._gen_url = f"{self.base}/api/generate"
        self._force_gen = force_generate

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def invoke(self, messages: List[BaseMessage]) -> AIMessage:
        """Send a list of LangChain ``BaseMessage`` objects and get the reply."""
        if self._force_gen:
            print(self.base, self._gen_url)
            return self._call_generate(messages)

        try:
            return self._call_chat(messages)
        except (requests.HTTPError, requests.Timeout, requests.ConnectionError) as e:
            # Any failure (404/405 *or* timeout etc.) → fallback to /api/generate
            if isinstance(e, requests.HTTPError) and e.response is not None:
                if e.response.status_code not in {404, 405}:
                    # For other HTTP codes re‑raise
                    raise
            # else: timeout / connection error → silent fallback
            return self._call_generate(messages)

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _call_chat(self, messages: List[BaseMessage]) -> AIMessage:
        payload = {
            "model": self.model,
            "messages": [self._to_openai(m) for m in messages],
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }
        r = requests.post(self._chat_url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        content = r.json()["message"]["content"]
        return AIMessage(content=content)

    def _call_generate(self, messages: List[BaseMessage]) -> AIMessage:
        prompt = self._flatten_prompt(messages)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "temperature": self.temperature,
            "top_p": self.top_p,
        }
        r = requests.post(self._gen_url, json=payload, timeout=self.timeout)
        r.raise_for_status()
        content = r.json()["response"]
        return AIMessage(content=content)

    # ------------------------------------------------------------------
    # Static utilities
    # ------------------------------------------------------------------
    @staticmethod
    def _to_openai(message: BaseMessage) -> dict:
        role_map = {
            SystemMessage: "system",
            HumanMessage: "user",
            AIMessage: "assistant",
        }
        return {"role": role_map[type(message)], "content": message.content}

    @staticmethod
    def _flatten_prompt(messages: List[BaseMessage], sep: str = "\n\n") -> str:
        parts: list[str] = []
        for m in messages:
            if isinstance(m, SystemMessage):
                parts.append(f"[system]\n{m.content}")
            elif isinstance(m, HumanMessage):
                parts.append(f"[user]\n{m.content}")
            elif isinstance(m, AIMessage):
                parts.append(f"[assistant]\n{m.content}")
        return sep.join(parts)


__all__ = ["OllamaChat"]
