import datetime
import os
import sys
from typing import Annotated

from sqlalchemy import func
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker
from sqlalchemy.orm import DeclarativeBase
from sqlalchemy.orm import Mapped, mapped_column
from contextlib import asynccontextmanager

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=True
)

async_session = async_sessionmaker(async_engine)

inpk = Annotated[int, mapped_column(primary_key=True, index=True)]
created_at = Annotated[datetime.datetime, mapped_column(server_default=func.now())]
updated_at = Annotated[datetime.datetime, mapped_column(server_default=func.now(), onupdate=datetime.datetime.now())]


class Base(DeclarativeBase):
    id: Mapped[inpk]
    created_at: Mapped[created_at]
    updated_at: Mapped[updated_at]


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session