# main.py
import os
from app.analyzer import DataAnalyzer
from app.models.model_factory import get_model_loader
from app.data_load import DataLoader
from app.core.config import settings

os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
def main():

    model = get_model_loader(settings.USE_OPENAI, api_key=settings.OPENAI_API_KEY)
    data_loader = DataLoader(settings.PATH_TO_DATA)
    analyzer = DataAnalyzer(model, data_loader=data_loader)
    
    print("📊 Добро пожаловать в консольную систему анализа данных!")
    print("Введите 'выход' или 'exit', чтобы завершить работу.\n")
    while True:
        user_input = input(" Задайте вопрос: ").strip()

        if user_input.lower() in ("выход", "exit", "quit"):
            print("\n До свидания!")
            break

        print("\n Обработка запроса...\n")
        try:
            answer = analyzer.ask(user_input)
        except Exception as e:
            answer = "Модель в данный момент не доступна. Обратитесь к администратору"
        print(f"{answer}\n")

if __name__ == "__main__":
    main()