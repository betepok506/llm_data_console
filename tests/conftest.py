# conftest.py

import pytest
from unittest.mock import MagicMock
from app.core.config import settings

MOCK_RESPONSES = {
    "Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?": """
import pandas as pd
df = pd.read_csv("./data/freelancer_earnings_bd.csv")
experts = df[df["Experience_Level"] == "Expert"]
experts_less_100 = experts[experts["Job_Completed"] < 100]
percentage = len(experts_less_100) / len(experts) * 100 if len(experts) > 0 else 0
result = f"Процент экспертов, выполнивших менее 100 проектов: {percentage:.2f}%"
""",
    "Какой уровень опыта чаще получает высокий рейтинг (>= 4.5)?": """
import pandas as pd
df = pd.read_csv("./data/freelancer_earnings_bd.csv")
high_rated = df[df["Client_Rating"] >= 4.5]
experience_counts = high_rated["Experience_Level"].value_counts()
most_common_exp_level = experience_counts.idxmax() if not experience_counts.empty else "Нет данных"
result = f"Чаще всего высокий рейтинг получают фрилансеры уровня: {most_common_exp_level}"
""",
}


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
