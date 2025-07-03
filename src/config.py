import os

from dotenv import load_dotenv
from pydantic_settings import BaseSettings, SettingsConfigDict

load_dotenv()


class Settings(BaseSettings):
    DB_HOST: str = "localhost"
    DB_PORT: str = "5432"
    DB_USER: str = "postgres"
    DB_PASSWORD: str = "123"
    DB_NAME: str = "aiogram"

    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASSWORD}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(env_file="../.env", extra="allow")


settings = Settings()

INSTAGRAM_USERNAME = os.getenv("INSTAGRAM_USERNAME")
INSTAGRAM_PASSWORD = os.getenv("INSTAGRAM_PASSWORD")

INSTAGRAM_USERNAME_SCHEDULER = os.getenv("INSTAGRAM_USERNAME_SCHEDULER")
INSTAGRAM_PASSWORD_SCHEDULER = os.getenv("INSTAGRAM_PASSWORD_SCHEDULER")

BOT_TOKEN = os.environ.get('BOT_TOKEN')
CHAT_ID = os.environ.get('CHAT_ID')

AUTO_REFRESH_STORIES = int(os.environ.get('AUTO_REFRESH_STORIES'))
AUTO_REFRESH_STATUS_ACC = int(os.environ.get('AUTO_REFRESH_STATUS_ACC'))

DAILY_DOWNLOAD_COUNT = int(os.environ.get('DAILY_DOWNLOAD_COUNT'))

FOLLOW_COUNT = int(os.environ.get('FOLLOW_COUNT'))