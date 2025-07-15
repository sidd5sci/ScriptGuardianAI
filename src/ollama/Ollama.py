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

OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434")

class OllamaChat:  # pylint: disable=too-few-public-methods
    """Interact with a locally running Ollama server.

    Parameters
    ----------
    model : str
        Ollama model identifier (e.g. ``"gemma:2b"`` or a Hugging Face GGUF
        path such as ``"hf.co/repo/model:Q4_K_M"``).
    temperature : float, optional
        Sampling temperature, by default 0.0 (deterministic).
    host : str, optional
        Base host URL, without the endpoint path. Defaults to
        ``"http://localhost:11434"``.
    top_p : float, optional
        Nucleus sampling parameter, by default 0.9.
    timeout : int, optional
        Requests timeout in seconds, default 600.
    """

    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        top_p: float = 0.9,
        timeout: int = 600,
    ) -> None:
        self.model = model
        self.temperature = float(temperature)
        self.base = OLLAMA_URL
        self.top_p = top_p
        self.timeout = timeout

        # Endpoint URLs
        self._chat_url = f"{self.base}/api/chat"
        self._gen_url = f"{self.base}/api/generate"

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def invoke(self, messages: List[BaseMessage]) -> AIMessage:  # noqa: D401
        """Send a batch of messages and return the assistant's reply."""
        try:
            return self._call_chat(messages)
        except requests.HTTPError as err:
            if err.response.status_code in {404, 405}:
                # Fallback to /api/generate for older Ollama versions.
                return self._call_generate(messages)
            raise

    # ------------------------------------------------------------------
    # Internals – new /api/chat path
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
        resp = requests.post(self._chat_url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        data = resp.json()
        # /api/chat returns {"message": {"role": "assistant", "content": "..."}, ...}
        content = data["message"]["content"]
        return AIMessage(content=content)

    # ------------------------------------------------------------------
    # Internals – legacy /api/generate path
    # ------------------------------------------------------------------
    def _call_generate(self, messages: List[BaseMessage]) -> AIMessage:
        prompt = self._flatten_prompt(messages)
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }
        resp = requests.post(self._gen_url, json=payload, timeout=self.timeout)
        resp.raise_for_status()
        content = resp.json()["response"]
        return AIMessage(content=content)

    # ------------------------------------------------------------------
    # Helper methods
    # ------------------------------------------------------------------
    @staticmethod
    def _to_openai(message: BaseMessage) -> Dict[str, str]:
        if isinstance(message, SystemMessage):
            role = "system"
        elif isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")
        return {"role": role, "content": message.content}

    @staticmethod
    def _flatten_prompt(messages: List[BaseMessage]) -> str:
        """Convert role‑based messages into a single prompt for /api/generate."""
        parts: list[str] = []
        for m in messages:
            if isinstance(m, SystemMessage):
                parts.append(m.content.strip())
            elif isinstance(m, HumanMessage):
                parts.append(f"User: {m.content.strip()}")
            elif isinstance(m, AIMessage):
                parts.append(f"Assistant: {m.content.strip()}")
        return "\n\n".join(parts) + "\nAssistant:"
