# app/openai_model.py


from openai import OpenAI

from app.models.base_model import ModelInterface


class OpenAIModelLoader(ModelInterface):
    """
    Реализация ModelInterface для взаимодействия с OpenAI API.
    """

    def __init__(
        self,
        api_key: str,
        model_name: str = "meta-llama/llama-3.3-8b-instruct:free",
        base_url: str = "https://openrouter.ai/api/v1",
        max_tokens: int = 500,
    ):
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model_name
        self.max_tokens = max_tokens

    def generate(self, prompt):
        """
        Генерирует ответ на основе промпта.

        Parameters
        ----------
        prompt : str
            Промпт, отправляемый модели.

        Returns
        -------
        dict
            Ответ модели в виде словаря с ключом "generated_text".
        """
        response = self.client.chat.completions.create(
            model=self.model_name,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=self.max_tokens,
            temperature=0.1,
        )
        return {"generated_text": response.choices[0].message.content}
