from pydantic_settings import BaseSettings
from os import getenv as ENV


class Settings(BaseSettings):
    DB_USER = ENV("DB_USER")
    DB_PASS = ENV("DB_PASS")
    DB_ENV = ENV("DB_ENV")
    DB_NAME = ENV("DB_NAME")

    SECRET_KEY = ENV("SECRET_KEY")
    ALGORITHM = ENV("ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES = ENV("ACCESS_TOKEN_EXPIRE_MINUTES")

    database_url: str = f"postgresql://{DB_USER}:{DB_PASS}@{DB_ENV}:5432/{DB_NAME}"
    secret_key: str = SECRET_KEY
    algorithm: str = ALGORITHM
    access_token_expire_minutes: int = ACCESS_TOKEN_EXPIRE_MINUTES

    class Config:
        env_file = ".env"


settings = Settings()
