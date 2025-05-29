from abc import ABC, abstractmethod


class ModelInterface(ABC):
    @abstractmethod
    def generate(self, prompt: str) -> str:
        """Генерирует Python-код на основе вопроса"""
        pass
