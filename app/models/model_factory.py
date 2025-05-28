# app/model_factory.py

from app.models.local_model import LocalModelLoader
from app.models.openai_model import OpenAIModelLoader
import os


def get_model_loader(
    use_openai: bool = True, api_key=None, model_name=None, max_tokens: int = 200
):
    if use_openai:
        return OpenAIModelLoader(api_key=api_key)
    else:
        return LocalModelLoader(model_name=model_name)
