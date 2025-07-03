import datetime

from sqlalchemy import and_, update
from sqlalchemy.future import select

from src.config import FOLLOW_COUNT
from src.database.base import get_session
from src.database.models import AutoFetchStories


async def add_or_replace_autofetch_account(tg_id: int, username: str):
    async with get_session() as session:
        result = await session.execute(
            select(AutoFetchStories)
            .where(and_(AutoFetchStories.user_id == tg_id)))
        follows = result.scalars().all()

        if any(f.account == username for f in follows):
            return True

        if len(follows) < FOLLOW_COUNT:
            new_follow = AutoFetchStories(
                user_id=tg_id,
                account=username
            )
            session.add(new_follow)
            await session.commit()
            return False


async def remove_follow(tg_id: int, username: str):
    async with get_session() as session:
        result = await session.execute(
            select(AutoFetchStories).where(
                and_(
                    AutoFetchStories.user_id == tg_id,
                    AutoFetchStories.account == username
                )
            )
        )
        follows = result.scalars().first()

        if follows:
            await session.delete(follows)
            await session.commit()


async def get_autofetch_accounts(tg_id: int) -> list[str]:
    async with get_session() as session:
        result = await session.execute(
            select(AutoFetchStories.account).where(and_(AutoFetchStories.user_id == tg_id)))

        return [row[0] for row in result.fetchall()]


async def get_last_story_time(tg_id: int, username: str) -> datetime:
    async with get_session() as session:
        result = await session.execute(
            select(AutoFetchStories.last_time)
            .where(and_(
                        AutoFetchStories.account == username,
                        AutoFetchStories.user_id == tg_id
                        )
                   )
            )
        last_time = result.scalar_one_or_none()
        return last_time


async def update_last_story_time(tg_id: int, username: str, new_time: datetime):
    async with get_session() as session:
        await session.execute(
            update(AutoFetchStories)
            .where(and_(AutoFetchStories.user_id == tg_id,
                        AutoFetchStories.account == username
                        )
                   )
            .values(last_time=new_time)
        )
        await session.commit()
