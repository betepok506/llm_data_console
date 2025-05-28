# app/cli.py

from analyzer import DataAnalyzer


class ConsoleApp:
    def __init__(self, analyzer: DataAnalyzer):
        self.analyzer = analyzer

    def run(self):
        print("📊 Добро пожаловать в консольную систему анализа данных!")
        print("Введите 'выход' или 'exit', чтобы завершить работу.\n")

        while True:
            user_input = input(" Задайте вопрос: ").strip()

            if user_input.lower() in ("выход", "exit", "quit"):
                print("\n До свидания!")
                break

            print("\n Обработка запроса...\n")
            answer = self.analyzer.ask(user_input)
            print(f"{answer}\n")
