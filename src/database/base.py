import os
import sys
from datetime import datetime
from contextlib import asynccontextmanager
from sqlalchemy.orm import DeclarativeBase, Mapped, mapped_column
from sqlalchemy.ext.asyncio import create_async_engine, async_sessionmaker

sys.path.append(os.path.abspath(os.path.dirname(__file__)))
from src.config.config import settings

async_engine = create_async_engine(
    url=settings.DATABASE_URL_asyncpg,
    echo=False
)
async_session = async_sessionmaker(async_engine)


class Base(DeclarativeBase):
    id: Mapped[int] = mapped_column(primary_key=True, index=True)
    created_at: Mapped[datetime] = mapped_column(default=datetime.utcnow)
    updated_at: Mapped[datetime] = mapped_column(default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)


@asynccontextmanager
async def get_session():
    async with async_session() as session:
        async with session.begin():
            yield session