
from __future__ import annotations
import os
import requests
from langchain_core.messages import SystemMessage, HumanMessage, AIMessage



class LMStudioChat:
    def __init__(self, model: str, temperature: float = 0.0, url: str = "http://127.0.0.1:1234/v1/chat/completions"):
        self.model = model
        self.temperature = temperature
        self.url = url
        self.repetition_penalty = 1.15
        self.top_p = 0.9


    def invoke(self, messages):
        openai_messages = []
        for m in messages:
            if isinstance(m, SystemMessage):
                role = "system"
            elif isinstance(m, HumanMessage):
                role = "user"
            elif isinstance(m, AIMessage):
                role = "assistant"
            else:
                raise ValueError(f"Unsupported message type: {type(m)}")
            openai_messages.append({"role": role, "content": m.content})

        payload = {
            "model": self.model,
            "messages": openai_messages,
            "temperature": self.temperature,
            "stream": False
        }

        # print("DEBUG Payload:", json.dumps(payload, indent=2))

        response = requests.post(self.url, json=payload)
        if response.status_code != 200:
            print("LM Studio error response:")
            print(response.text)
        response.raise_for_status()

        result = response.json()
        return AIMessage(content=result["choices"][0]["message"]["content"])
