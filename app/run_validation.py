import pandas as pd

from app.analyzer import DataAnalyzer
from app.core.config import settings
from app.data_load import DataLoader
from app.models.model_factory import get_model_loader
import jsonlines
import json
import re

def execute_code(code_str, verbose=False):
    """
    Безопасное выполнение Python-кода и получение переменной result.
    """
    globals_dict = {}
    locals_dict = {}

    try:
        exec(code_str, globals_dict, locals_dict)
        result = locals_dict.get("result", None)
        if verbose:
            print(f"✅ Результат выполнения: {result}")
        return result
    except Exception as e:
        print(f"❌ Ошибка выполнения: {e}")
        return None

def load_jsonl(file_path):
    with jsonlines.open(file_path) as reader: 
        data = [obj for obj in reader]
    return data

def load_validation_answers(file_path):
    with open(file_path, "r", encoding="utf-8") as f:
        data = json.load(f)
    return data

def compare_results(predicted, expected):
    """
    Сравнивает два результата — как строки или числа.
    """
    try:
        # Попробуем привести к float
        predicted_num = float(str(predicted).strip('%').replace(',', '.')) if predicted else None
        expected_num = float(str(expected).strip('%').replace(',', '.')) if expected else None
        return abs(predicted_num - expected_num) < 1e-2
    except:
        # Если не число — сравниваем как строки
        return str(predicted).strip() == str(expected).strip()

def extract_numbers(text):
    # Находим все числа, включая дробные
    return list(map(float, re.findall(r"[-+]?\d*\.\d+|\d+", text)))

def evaluate_answers(history_data, validation_data):
    correct_count = 0
    total_count = 0

    for entry in history_data:
        question = entry["question"]
        generated_code = entry["code"]

        # Проверяем, есть ли такой вопрос в эталонных ответах
        if question not in validation_data:
            print(f"❓ Вопрос отсутствует в эталонных данных: {question}")
            continue

        reference_code = validation_data[question]
        print(f"\n🔄 Обрабатываем вопрос: {question}")

        # Выполняем сгенерированный код
        generated_result = execute_code(generated_code)
        expected_result = execute_code(reference_code)

        print(f'Сгенерированный результат: {generated_result}')
        if generated_result.find(":") != -1:
            generated_result = generated_result.split(":", 1)[1]
            
        generated_result = extract_numbers(generated_result)[0]
        # Сравниваем результаты
        match = compare_results(generated_result, expected_result)

        print(f"Извлеченный ответ из сгенерированного результата: {generated_result}")
        print(f"Эталонный результат: {expected_result}")
        print(f"Результат совпадает: {'✅' if match else '❌'}")

        total_count += 1
        if match:
            correct_count += 1

    accuracy = correct_count / total_count if total_count > 0 else 0
    print(f"\n📊 Точность: {accuracy:.2%} ({correct_count}/{total_count})")
    return accuracy


if __name__ == "__main__":
    history_data = load_jsonl("./data/history.json")
    validation_data = load_validation_answers("./data/validate_answer.json")

    evaluate_answers(history_data, validation_data)

