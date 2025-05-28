# tests/test_analyzer.py

import pytest
import pandas as pd
from app.analyzer import DataAnalyzer
from app.data_load import DataLoader
from app.models.local_model import LocalModel
from tests.utils.compare import compare_numbers

@pytest.fixture
def analyzer():
    model = LocalModel()
    data_loader = DataLoader("./data/freelancer_earnings.csv")
    return DataAnalyzer(model, data_loader)

@pytest.mark.parametrize("question, expected", [
    ("Какой средний доход у фрилансеров из Европы?", "6500"),
    ("Какой уровень опыта чаще получает высокий рейтинг (>=4.5)?", "Expert"),
    ("Насколько выше почасовая ставка у тех, кто принимает криптовалюту?", "На 8.3$"),
    ("Какой процент фрилансеров — эксперты, но выполнили менее 100 проектов?", "18.75%"),
])
def test_analyzer(analyzer, question, expected):
    answer = analyzer.ask(question)

    # Проверяем числа, если они есть в ожидаемом результате
    if any(char.isdigit() for char in expected):
        assert compare_numbers(expected, answer), f"Число в ответе '{answer}' не совпадает с эталоном '{expected}'"
    else:
        # Если это не число, просто сравниваем строку
        assert expected.lower() in answer.lower(), f"Ответ '{answer}' не содержит '{expected}'"

    print(f"✅ Вопрос: {question}")
    print(f"➡️ Ответ: {answer}")
    print("-" * 50)