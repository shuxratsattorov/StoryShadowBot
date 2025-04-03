import os
import sys
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    pass
