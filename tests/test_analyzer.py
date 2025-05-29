# tests/test_analyzer.py

import pytest
from app.analyzer import DataAnalyzer


# @pytest.fixture
# def analyzer():
#     model = LocalModel()
#     data_loader = DataLoader("./data/freelancer_earnings.csv")
#     return DataAnalyzer(model, data_loader)


@pytest.mark.parametrize(
    "question, expected",
    [
        (
            "Какой процент фрилансеров, считающих себя экспертами, выполнил менее 100 проектов?",
            "33.85%",
        ),
        (
            "Какой уровень опыта чаще получает высокий рейтинг (>= 4.5)?",
            "Intermediate",
        ),
    ],
)
def test_analyzer_with_mocked_model(
    mocked_model, data_loader, question, expected
):
    """
    Тестирует DataAnalyzer с замоканной моделью.
    """
    analyzer = DataAnalyzer(model_loader=mocked_model, data_loader=data_loader)

    print(f"\n🧪 Тестируем вопрос: {question}")
    actual_answer = analyzer.ask(question)

    print(f"➡️ Ответ системы:\n{actual_answer}")

    assert (
        expected.lower() in actual_answer.lower()
    ), f"Ответ '{actual_answer}' не содержит '{expected}'"
