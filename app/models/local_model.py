# app/model_loader.py

from transformers import AutoModelForCausalLM, AutoTokenizer, pipeline
# from app.models import ModelLoader

class LocalModelLoader:
    def __init__(self, model_name: str, max_tokens: int = 200, temperature: float = 0.3):
        # Написать дескрипторы
        self.model_name = model_name
        self.tokenizer, self.model, self.llm = self._load_model()
        self.max_tokens=max_tokens
        self.temperature = temperature

    def _load_model(self):
        tokenizer = AutoTokenizer.from_pretrained(self.model_name)
        model = AutoModelForCausalLM.from_pretrained(self.model_name)
        llm = pipeline(
            "text-generation",
            model=model,
            tokenizer=tokenizer,
            max_new_tokens=self.max_tokens,
            temperature=self.temperature
        )
        return tokenizer, model, llm