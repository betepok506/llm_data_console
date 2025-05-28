
from abc import ABC, abstractmethod

class ModelInterface(ABC):
    @abstractmethod
    def generate_code(self, question: str) -> str:
        """Генерирует Python-код на основе вопроса"""
        pass