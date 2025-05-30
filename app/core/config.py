from enum import Enum

from pydantic_settings import BaseSettings


class ModeEnum(str, Enum):
    development = "development"
    production = "production"
    testing = "testing"


class Settings(BaseSettings):
    # PROJECT_NAME: str
    USE_OPENAI: bool = True
    PATH_TO_DATA: str = "./data/freelancer_earnings_bd.csv"
    MODEL_NAME: str = "meta-llama/llama-3-8b-instruct:free"
    OPENAI_API_KEY: str | None = None
    PATH_TO_PROMPT_CONFIG: str = "./app/prompts/prompt_config.json"

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"
        extra = "ignore"


settings = Settings()
