from pydantic import SecretStr
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    SECRET_KEY: str
    ALGORITHM: str


    class Config:
        env_file = '.env'
        env_file_encoding = 'utf-8'

settings = Settings()
