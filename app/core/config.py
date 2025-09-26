from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DB_USER: str = Field(..., env="DB_USER")
    DB_PASS: str = Field(..., env="DB_PASS")
    DB_ENV: str = Field(..., env="DB_ENV")
    DB_NAME: str = Field(..., env="DB_NAME")

    SECRET_KEY: str = Field(..., env="SECRET_KEY")
    ALGORITHM: str = Field(..., env="ALGORITHM")
    ACCESS_TOKEN_EXPIRE_MINUTES: str = Field(..., env="ACCESS_TOKEN_EXPIRE_MINUTES")

    @property
    def database_url(self) -> str:
        return f"postgresql://{self.DB_USER}:{self.DB_PASS}@{self.DB_ENV}:5432/{self.DB_NAME}"

    @property
    def secret_key(self) -> str:
        return self.SECRET_KEY

    @property
    def algorithm(self) -> str:
        return self.ALGORITHM

    @property
    def access_token_expire_minutes(self) -> int:
        return int(self.ACCESS_TOKEN_EXPIRE_MINUTES)

    class Config:
        env_file = ".env"


settings = Settings()
