import pytz
import datetime
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    #   < --- Postgres --- >
    DB_HOST: str
    DB_PORT: str
    DB_USER: str
    DB_PASS: str
    DB_NAME: str

    #   < --- Redis --- >
    REDIS_BROKER_URL: str
    REDIS_BACKEND_URL: str

    #   < --- Telegram Bot --- >
    BOT_TOKEN: str
    CHAT_ID: int

    #   < --- Config --- >
    DAILY_DOWNLOAD_COUNT: int
    FOLLOW_COUNT: int

    #   < --- Config --- >
    AUTO_REFRESH_STORIES: int
    AUTO_REFRESH_STATUS_ACC: int

    #   < --- JWT --- >
    JWT_SECRET_KEY: str | None = None
    JWT_ALGORITHM: str | None = None

    #   < --- DEBUG --- >
    DEBUG: bool

    #   < --- DOMAIN --- >
    DOMAIN: str | None = None
    API_DOMAIN: str | None = None


    @property
    def DATABASE_URL_asyncpg(self):
        return f"postgresql+asyncpg://{self.DB_USER}:{self.DB_PASS}@{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"

    model_config = SettingsConfigDict(
        env_file=(Path(__file__).resolve().parents[2] / ".env"), 
        extra="allow"
        )


settings = Settings()


toshkent_tz = pytz.timezone('Asia/Tashkent')

def current_time(time_zone=True):
    if time_zone:
        return datetime.datetime.now(tz=toshkent_tz)
    else:
        return datetime.datetime.now()


origins = [
    
]

if settings.DEBUG:
    origins.extend([
        
    ])