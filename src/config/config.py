import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    #   < --- Postgres --- >
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    DB_NAME: str = "aiogram"

    #   < --- Redis --- >
    REDIS_BROKER_URL: str = "redis://localhost:6379/0"
    REDIS_BACKEND_URL: str = "redis://localhost:6379/1"

    #   < --- Telegram Bot --- >
    BOT_TOKEN: str = ""
    CHAT_ID: int = ""

    #   < --- Config --- >
    DAILY_DOWNLOAD_COUNT: int = ""
    FOLLOW_COUNT: int = ""

    #   < --- Config --- >
    AUTO_REFRESH_STORIES: int = ""
    AUTO_REFRESH_STATUS_ACC: int = ""

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env", extra="allow")


settings = Settings()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

INSTAGRAM_USERNAME_SCHEDULER = os.getenv("INSTAGRAM_USERNAME_SCHEDULER")
INSTAGRAM_PASSWORD_SCHEDULER = os.getenv("INSTAGRAM_PASSWORD_SCHEDULER")