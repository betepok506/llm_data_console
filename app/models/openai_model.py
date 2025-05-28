# app/openai_model.py

import os
from openai import OpenAI


class OpenAIModelLoader:
    def __init__(
        self,
        api_key: str,
        model_name: str = "meta-llama/llama-3.3-8b-instruct:free",
        base_url: str = "https://openrouter.ai/api/v1",
        max_tokens: int = 200,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.max_tokens = max_tokens

    def llm(self, prompt):
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
        )
        return [{"generated_text": response.choices[0].message.content}]
