import os
import sys
from contextlib import asynccontextmanager
from datetime import datetime

from sqlalchemy.ext.asyncio import async_sessionmaker
from sqlalchemy.ext.asyncio import create_async_engine
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from typing_extensions import Annotated

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

async_session = async_sessionmaker(async_engine)

inpk = Annotated[int, mapped_column(primary_key=True, index=True)]


class Base(DeclarativeBase):
    id: Mapped[inpk]
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session