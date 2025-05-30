# analyzer.py
from app.core.config import settings
from app.data_load import DataLoader
from app.prompts.loader import format_examples, load_prompt_config
from app.responses import MESSAGE_ERROR
from app.utils import format_answer

# Загружаем данные для промпта
PROMPT_CONFIG = load_prompt_config(settings.PATH_TO_PROMPT_CONFIG)
DATASET_SCHEMA_DESCRIPTION = PROMPT_CONFIG["schema_description"]
INSTRUCTIONS = PROMPT_CONFIG["instructions"]
EXAMPLES = format_examples(PROMPT_CONFIG["examples"])


class DataAnalyzer:
    """
    Класс для анализа данных на основе вопросов пользователя и
    генерации ответов через LLM (например, OpenAI).
    """

    def __init__(self, model_loader, data_loader: DataLoader):
        """
        Инициализирует объект DataAnalyzer.

        Parameters
        ----------
        model_loader : ModelInterface
            Объект, предоставляющий метод generate().
        data_loader : DataLoader
            Объект, предоставляющий доступ к данным.
        """
        self.model_loader = model_loader
        self.data = data_loader.data
        self.prompt = None

    def ask(self, question: str, return_code: bool = False):
        """
        Генерирует Python-скрипт на основе вопроса и выполняет его.

        Parameters
        ----------
        question : str
            Вопрос пользователя на естественном языке.
        return_code : bool, optional
            Если True, возвращает и ответ, и сгенерированный код, by
            default False

        Returns
        -------
        dict
            Словарь с ключом 'answer' и, опционально, 'code'.
        """
        prompt = (
            f"{DATASET_SCHEMA_DESCRIPTION}\n"
            f"{INSTRUCTIONS}\n\n"
            f'Вопрос: "{question}"\n'
            "Код:"
        )

        response = self.model_loader.generate(prompt)
        code = response["generated_text"]

        local_vars = {"df": self.data, "result": None}
        if "./data/freelancer_earnings_bd.csv" not in code:
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
                "str": str,
            }
            globals_dict = {"__builtins__": safe_builtins}
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
        except Exception:
            return {
                "answer": MESSAGE_ERROR,
                "code": None,
            }
