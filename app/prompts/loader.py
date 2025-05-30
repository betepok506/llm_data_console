# app/prompts/loader.py
import json
import os


def load_prompt_config(path_to_file):
    if not os.path.exists(path_to_file):
        raise FileNotFoundError(f"Файл конфига не найден: {path_to_file}")
    with open(path_to_file, "r", encoding="utf-8") as f:
        return json.load(f)


def format_examples(examples):
    formatted = []
    for i, example in enumerate(examples):
        code = example.strip()
        formatted.append(f"Пример {i + 1}\n" f"\n{code}\n")
    return "\n\n".join(formatted)
