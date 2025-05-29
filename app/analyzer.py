# analyzer.py
from app.data_load import DataLoader
from app.utils import format_answer
from app.schema import DATASET_SCHEMA_DESCRIPTION, MESSAGE_ERROR  # <-- Импорт схемы


class DataAnalyzer:
    def __init__(self, model_loader, data_loader: DataLoader):
        self.model_loader = model_loader
        self.data = data_loader.data

    def ask(self, question: str, return_code: bool = False):
        schema_desc = DATASET_SCHEMA_DESCRIPTION

        prompt = f"""
        {schema_desc}

        Преобразуй следующий вопрос в Python скрипт, который можно
        выполнить функцией eval().
        В ответном сообщении ты должен написать только код, который
        не должен быть никак отформатирован.
        Скрипт должен быть написан только с испольщованием библиотеки pandas.
        Ты должен написать код, который:
        - Считает датасет из каталога "./data/freelancer_earnings_bd.csv"
        - Произведет запрос к данным, учитывая при этом запросы пользователя
        - Сохранит результаты в переменную result
        - Учти, что вывод результата должен форматироваться соглассно
        запросу пользователя чтобы его удобно читать.
        - Дополни ответ комментариями и сохрани его ввиде строки в
        переменную result
        - Код должен использовать **только pandas** для анализа данных.
        - Все вычисления должны быть завершены внутри кода.
        - Не создавай тестовые данные, не используй mock-библиотеки.

        Категорически запрещается делать следующее:
        - Генерировать код который может модифицировать/удалять/изменять
        данные из файла.
        - Генерировать код который может удалять/переименовывать/копировать/перемещать
        набора данных.
        - Генерировать какой либо код, кроме того, который будет взаимодействовать с набором данных pandas

        Если запрос запрещен, то выдай ответ "Я не могу выполнить запрос такого рода"
        Если ты не можешь выполнить запрос напиши - "Мне не удалось получить ответ на ваш вопрос.
        Постарайтесь уточнить его." и сохрани его в переменную result

        Ниже приведены примеры сгенерированного кода:

        Пример 1
        import pandas as pd

        # Загрузка данных
        df = pd.read_csv("./data/freelancer_earnings_bd.csv")

        # Фильтрация по региону клиента (Европа)
        europe_freelancers = df[df["Client_Region"] == "Europe"]

        # Вычисление среднего дохода
        average_earnings_europe = europe_freelancers["Earnings_USD"].mean()

        result = f"Средний доход фрилансеров с клиентами из Европы: " + average_earnings_europe + " USD" # noqa: E501

        Пример 2

        import pandas as pd

        # Загрузка данных
        df = pd.read_csv("./data/freelancer_earnings_bd.csv")

        # Фильтрация фрилансеров с рейтингом >= 4.5
        high_rated = df[df["Client_Rating"] >= 4.5]

        # Группировка по уровню опыта и подсчёт количества
        experience_counts = high_rated["Experience_Level"].value_counts()

        # Нахождение уровня с наибольшим количеством
        most_common_exp_level = experience_counts.idxmax()
        count = experience_counts.max()

        result = "Чаще всего высокий рейтинг получают фрилансеры уровня: " + most_common_exp_level # noqa: E501
        result += f"Количество таких фрилансеров: " + count


        Вопрос: "{question}"

        Код:
        """

        response = self.model_loader.generate(prompt)
        code = response["generated_text"]

        local_vars = {"df": self.data, "result": None}
        if not "./data/freelancer_earnings_bd.csv" in code:
            return {
                "answer": format_answer(question, MESSAGE_ERROR),
                "code": None,
            }
            
        try:
            safe_builtins = {
                "__import__": __import__,
                "len": len,
                "round": round,
                "sum": sum,
                "min": min,
                "max": max,
                "abs": abs,
            }
            globals_dict = {
                "__builtins__": safe_builtins
            }
            exec(code, globals_dict, local_vars)
            result = local_vars.get("result", "Не удалось вычислить")
            if result is None:
                result = MESSAGE_ERROR
            if not return_code:
                return {"answer": format_answer(question, result)}
            else:
                return {
                    "answer": format_answer(question, result),
                    "code": code,
                }
        except Exception as e:
            return {
                "answer": MESSAGE_ERROR,
                "code": None,
            }
