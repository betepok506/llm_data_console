import pandas as pd

from app.analyzer import DataAnalyzer
from app.core.config import settings
from app.data_load import DataLoader
from app.models.model_factory import get_model_loader


def run_tests():
    model = get_model_loader(
        settings.USE_OPENAI, api_key=settings.OPENAI_API_KEY
    )
    data_loader = DataLoader(settings.PATH_TO_DATA)
    analyzer = DataAnalyzer(model, data_loader=data_loader)

    tests = pd.read_csv("./data/test_questions.csv")

    results = []

    for _, row in tests.iterrows():
        question = row["question"]
        expected = row["expected_answer"]

        try:
            answer = analyzer.ask(question)
            passed = str(expected).lower() in answer.lower()
        except Exception as e:
            answer = f"Ошибка: {str(e)}"
            passed = False

        results.append(
            {
                "question": question,
                "expected": expected,
                "actual": answer,
                "passed": passed,
            }
        )

    results_df = pd.DataFrame(results)
    results_df.to_csv("./data/report.csv", index=False)

    print(f"✅ Пройдено: {results_df['passed'].sum()} из {len(results_df)}")
    print("📄 Детали сохранены в ./data/report.csv")


if __name__ == "__main__":
    run_tests()
