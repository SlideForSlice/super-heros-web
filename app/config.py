import os

from dotenv import load_dotenv
from pydantic import SecretStr
from pydantic.v1 import root_validator
from pydantic_settings import BaseSettings
from typing import Literal

from dotenv import load_dotenv
load_dotenv()

class Settings(BaseSettings):
    MODE: Literal['DEV', 'TEST']

    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    TEST_DB_HOST: str
    TEST_DB_PORT: int
    TEST_DB_USER: str
    TEST_DB_PASS: str
    TEST_DB_NAME: str

    SMTP_HOST: str
    SMTP_PORT: int
    SMTP_USER: str
    SMTP_PASS: str

    REDIS_URL: str

    SECRET_KEY: str
    ALGORITHM: str

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
    }

settings = Settings()

