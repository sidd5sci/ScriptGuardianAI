"""A thin Ollama chat wrapper compatible with LangChain-style messages.

Example
-------
>>> from langchain_core.messages import SystemMessage, HumanMessage
>>> chat = OllamaChat(model="gemma:2b")
>>> reply = chat.invoke([
...     SystemMessage(content="You are a helpful assistant."),
...     HumanMessage(content="Hello, what's 2+2?")
... ])
>>> print(reply.content)
'4'
"""
from __future__ import annotations

import json
import requests
from typing import List

from langchain_core.messages import SystemMessage, HumanMessage, AIMessage, BaseMessage


class OllamaChat:  # pylint: disable=too-few-public-methods
    """Interact with a locally running Ollama server using its /api/chat endpoint.

    Parameters
    ----------
    model : str
        The exact Ollama model identifier, e.g. ``"gemma:2b"`` or ``"llama3:instruct"``.
    temperature : float, optional
        Sampling temperature, by default 0.0 (deterministic).
    url : str, optional
        Base *chat* endpoint; defaults to ``"http://localhost:11434/api/chat"``.
    top_p : float, optional
        Nucleus sampling parameter, by default 0.9.
    """

    def __init__(
        self,
        model: str,
        temperature: float = 0.0,
        url: str = "http://localhost:11434/api/chat",
        top_p: float = 0.9,
    ) -> None:
        self.model = model
        self.temperature = float(temperature)
        self.url = url.rstrip("/")  # remove trailing slash if given
        self.top_p = top_p

    # ---------------------------------------------------------------------
    # Public API
    # ---------------------------------------------------------------------
    def invoke(self, messages: List[BaseMessage]) -> AIMessage:
        """Send a list of LangChain ``BaseMessage`` objects to Ollama and return the reply.

        The function blocks until a full response is available (``stream = False``).
        """
        openai_messages = [self._to_openai(m) for m in messages]

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "stream": False,
            "options": {
                "temperature": self.temperature,
                "top_p": self.top_p,
            },
        }

        resp = requests.post(self.url, json=payload, timeout=600)
        try:
            resp.raise_for_status()
        except requests.HTTPError as err:
            raise RuntimeError(f"Ollama error {resp.status_code}: {resp.text}") from err

        data = resp.json()
        # Ollama returns { "message": {"role": "assistant", "content": "..."}, ... }
        assistant_content = data["message"]["content"]
        return AIMessage(content=assistant_content)

    # ------------------------------------------------------------------
    # Helpers
    # ------------------------------------------------------------------
    @staticmethod
    def _to_openai(message: BaseMessage) -> dict:
        if isinstance(message, SystemMessage):
            role = "system"
        elif isinstance(message, HumanMessage):
            role = "user"
        elif isinstance(message, AIMessage):
            role = "assistant"
        else:
            raise ValueError(f"Unsupported message type: {type(message)}")
        return {"role": role, "content": message.content}


__all__ = ["OllamaChat"]
