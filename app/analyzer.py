# analyzer.py
import os
import logging
import pandas as pd
from app.data_load import DataLoader
from app.utils import format_answer

logger = logging.getLogger(__name__)

class DataAnalyzer:
    def __init__(self, model_loader, data_loader: DataLoader):
        self.model_loader = model_loader
        self.data = data_loader.data

    def ask(self, question: str):
        schema_desc = """
        Датасет содержит следующие колонки:
        - Freelancer_ID: уникальный идентификатор каждого фрилансера
        - Job_Category: Первичная классификация выполняемой внештатной работы. Тип данных string. Примеры: Web Development, Data Entry, Content Writing
        - Platform: Торговая площадка фрилансеров, на которой была выполнена работа. Тип данных string. Примеры: Fiverr, Upwork, Toptal, Freelancer, PeoplePerHour
        - Experience_Level: Уровень профессионального опыта фрилансера. Тип данных string. Примеры: Beginner, Intermediate, Expert
        - Client_Region: Географическое положение клиента. Тип данных string. Примеры: Asia, Europe, USA, Canada, UK, Australia, Middle East
        - Payment_Method: Метод, используемый для проведения финансовых операций. Тип данных string. Примеры: Bank Transfer, PayPal, Mobile Banking, Crypto
        - Job_Completed: Количество успешно завершенных проектов. Тип данных integer. Примеры: 180, 218, 27
        - Earnings_USD: Общая прибыль в долларах США. Тип данных float. Примеры: 1620, 9078, 3455
        - Hourly_Rate: Ставка почасовой оплаты труда фрилансера в долларах США. Тип данных float. Примеры: 95.79, 86.38, 85.17
        - Job_Success_Rate: Процент успешного выполнения заданий. Тип данных float. Примеры: 68.73, 97.54, 86.6
        - Client_Rating: Средняя оценка, данная клиентами (по шкале от 1,0 до 5,0). Тип данных float. Примеры: 3.18, 3.44, 4.2
        - Job_Duration_Days: Средний срок реализации проекта в днях. Тип данных integer. Примеры: 1, 54, 46
        - Project_Type: Классификация организации работ. Тип данных string. Примеры: Fixed, Hourly
        - Rehire_Rate: Процент клиентов, которые повторно нанимают фрилансера. Тип данных float. Примеры: 40.19, 36.53, 74.05
        - Marketing_Spend: Сумма инвестиций в продвижение платформы в долларах США. Тип данных integer. Примеры: 53, 486, 489
        """

        prompt = f"""
        {schema_desc}
        
        Преобразуй следующий вопрос в Python скрипт, который можно выполнить функцией eval(). 
        В ответном сообщении ты должен написать только код, который не должен быть никак отформатирован.
        Скрипт должен быть написан с испольщованием библиотеки pandas. 
        Ты должен написать код, который:
        - Считает датасет из каталога "./data/freelancer_earnings_bd.csv"
        - Произведет запрос к данным, учитывая при этом запросы пользователя
        - Сохранит результаты в переменную result
        - Учти, что вывод результата должен форматироваться соглассно запросу пользователя чтобы его удобно читать. 
        - Дополни ответ комментариями и сохрани его ввиде строки в переменную result
        
        Категорически запрещается делать следующее:
        - Генерировать код который может модифицировать/удалять/изменять данные из файла.
        - Генерировать код который может удалять/переименовывать/копировать/перемещать набора данных.
        
        Если запрос запрещен, то выдай ответ "Я не могу выполнить запрос такого рода"
        Если ты не можешь выполнить запрос напиши - "Мне не удалось получить ответ на ваш вопрос. Постарайтесь уточнить его." и сохрани его в переменную result
        
        Ниже приведены примеры сгенерированного кода:
        
        Пример 1
        import pandas as pd

        # Загрузка данных
        df = pd.read_csv("./data/freelancer_earnings_bd.csv")

        # Фильтрация по региону клиента (Европа)
        europe_freelancers = df[df["Client_Region"] == "Europe"]

        # Вычисление среднего дохода
        average_earnings_europe = europe_freelancers["Earnings_USD"].mean()

        result = f"Средний доход фрилансеров с клиентами из Европы: " + average_earnings_europe + " USD"
        
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

        result = "Чаще всего высокий рейтинг получают фрилансеры уровня: " + most_common_exp_level
        result += f"Количество таких фрилансеров: " + count
        
        
        Вопрос: "{question}"
        
        Код:
        """

        response = self.model_loader.llm(prompt)
        code = response[0]['generated_text']

        logger.debug(" Сенерированный код: \n {code}")

        local_vars = {'df': self.data, 'result': None}

        try:
            exec(code, globals(), local_vars)
            result = local_vars.get('result', 'Не удалось вычислить')
            if result is None:
                result = "Мне не удалось получить ответ на ваш вопрос. Постарайтесь уточнить его."
            return format_answer(question, result)
        except Exception as e:
            logger.error(f"Ошибка при выполнении запроса: {e}", exc_info=True)
            return f"❌ Ошибка при выполнении кода: {str(e)}"
