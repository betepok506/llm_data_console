# main.py
import json
import os
import time

from app.analyzer import DataAnalyzer
from app.core.config import settings
from app.data_load import DataLoader
from app.models.model_factory import get_model_loader
from app.responses import MESSAGE_ERROR

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY


def main():

    model = get_model_loader(
        settings.USE_OPENAI, api_key=settings.OPENAI_API_KEY
    )

    data_loader = DataLoader(settings.PATH_TO_DATA)
    analyzer = DataAnalyzer(model, data_loader=data_loader)

    print("Добро пожаловать в консольную систему анализа данных!")
    print("Введите 'выход' или 'exit', чтобы завершить работу.\n")
    total_time = 0
    num_requests = 0
    while True:
        user_input = input(" Задайте вопрос: ").strip()

        if user_input.lower() in ("выход", "exit", "quit"):
            print(f"Количество запросов к модели: {num_requests}")
            print(
                f"Среднее время ответа модели: \
                    {total_time/(num_requests + 0.0001)}"
            )
            print("\n До свидания!")
            break

        print("\n Обработка запроса...\n")
        try:
            start = time.time()
            answer = analyzer.ask(user_input, return_code=True)
            end = time.time()
            num_requests += 1
            total_time += end - start

        except Exception:
            answer = {}
            answer["answer"] = MESSAGE_ERROR

        try:
            # Сохраняем историю пользовательских запросов и ответов на них
            with open("./data/history.json", "a", encoding="utf-8") as f:
                json.dump(
                    {"question": user_input, **answer},
                    f,
                    ensure_ascii=False,
                )
                f.write("\n")
        except (json.JSONDecodeError, UnicodeDecodeError):
            # Если возникла ошибка при записи в файл - пропускаем
            pass

        print(f"{answer['answer']}\n")


if __name__ == "__main__":
    main()
