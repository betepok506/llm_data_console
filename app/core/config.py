import os
from enum import Enum
from pydantic_settings import BaseSettings, SettingsConfigDict


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
    OPENAI_API_KEY: str = os.getenv("USE_OPENAI")
    model_config = SettingsConfigDict(
        case_sensitive=True, env_file=os.path.expanduser("~/.env")
    )


settings = Settings()
