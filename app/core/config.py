import os
from enum import Enum

from pydantic_settings import BaseSettings


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    # PROJECT_NAME: str
    HF_HOME: str = "./models"
    USE_OPENAI: bool = os.getenv("USE_OPENAI")
    PATH_TO_DATA: str = os.getenv("PATH_TO_DATA")
    MODEL_NAME: str = os.getenv("MODEL_NAME")
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")
    PATH_TO_PROMPT_CONFIG: str = os.getenv("PATH_TO_PROMPT_CONFIG")

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
os.environ["OPENAI_API_KEY"] = settings.OPENAI_API_KEY
