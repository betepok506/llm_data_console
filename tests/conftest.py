# conftest.py

import pytest
from unittest.mock import MagicMock
from app.core.config import settings
import json
import os

# Путь к файлу с моками
MOCK_RESPONSES_PATH = "./tests/fixtures/mock_responses.json"


# Загружаем моки из файла
def load_mock_responses():
    if not os.path.exists(MOCK_RESPONSES_PATH):
        raise FileNotFoundError(f"Файл {MOCK_RESPONSES_PATH} не найден")
    with open(MOCK_RESPONSES_PATH, "r", encoding="utf-8") as f:
        return json.load(f)


MOCK_RESPONSES = load_mock_responses()


@pytest.fixture
def mocked_model():
    from app.models.base_model import ModelInterface

    def extract_question_from_prompt(prompt: str) -> str | None:
        import re

        match = re.search(r'Вопрос:\s*"(.*?)"', prompt, re.DOTALL)
        if match:
            return match.group(1).strip()
        return None

    def generate_code_mock(prompt):
        question = extract_question_from_prompt(prompt)
        if not question:
            raise ValueError("Не удалось извлечь вопрос из промпта")

        if question in MOCK_RESPONSES:
            return {"generated_text": MOCK_RESPONSES[question]}
        else:
            raise ValueError(f"Нет мока для вопроса: '{question}'")

    mock_model = MagicMock(spec=ModelInterface)
    mock_model.generate.side_effect = generate_code_mock
    return mock_model


@pytest.fixture
def data_loader():
    from app.data_load import DataLoader

    return DataLoader(settings.PATH_TO_DATA)
