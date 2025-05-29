# main.py
import json
import os

from app.analyzer import DataAnalyzer
from app.core.config import settings
from app.data_load import DataLoader
from app.models.model_factory import get_model_loader

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


def main():

    model = get_model_loader(
        settings.USE_OPENAI, api_key=settings.OPENAI_API_KEY
    )
    data_loader = DataLoader(settings.PATH_TO_DATA)
    analyzer = DataAnalyzer(model, data_loader=data_loader)

    print("Добро пожаловать в консольную систему анализа данных!")
    print("Введите 'выход' или 'exit', чтобы завершить работу.\n")
    while True:
        user_input = input(" Задайте вопрос: ").strip()

        if user_input.lower() in ("выход", "exit", "quit"):
            print("\n До свидания!")
            break

        print("\n Обработка запроса...\n")
        try:
            answer = analyzer.ask(user_input)
        except Exception:
            answer = "Модель в данный момент не доступна. \
            Обратитесь к администратору"

        # Сохраняем историю пользовательских запросов и ответов на них
        with open("./data/history.json", "a", encoding="utf-8") as f:
            json.dump(
                {"question": user_input, "answer": answer},
                f,
                ensure_ascii=False,
            )
            f.write("\n")

        print(f"{answer}\n")


if __name__ == "__main__":
    main()
