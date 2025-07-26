import datetime
from datetime import timedelta, date

from sqlalchemy import and_, func, update
from sqlalchemy.future import select

from src.config.config import settings
from src.database.base import get_async_session
from src.database.models.models import User, Search

daily_donwnload_count = settings.DAILY_DOWNLOAD_COUNT


async def add_user(tg_id: int, fullname: str, username: str):
    async with get_async_session() as session:
        result = await session.execute(select(User).where(and_(User.tg_id == tg_id)))
        user = result.scalars().first()

        if user is None:
            new_user = User(
                tg_id=tg_id,
                fullname=fullname,
                username=username,
            )
            session.add(new_user)
            await session.commit()
            return True
        else:
            return False


async def save_search_to_db(tg_id: int, search_query: str):
    async with get_async_session() as session:
        result = await session.execute(
            select(Search).where(and_(Search.user_id == tg_id, Search.search == search_query))
        )
        search_entry = result.scalars().first()

        if search_entry:
            search_entry.count += 1
        else:
            new_search = Search(
                user_id=tg_id,
                search=search_query
            )
            session.add(new_search)

        await session.commit()


async def get_user_statistics():
    async with get_async_session() as session:
        now = datetime.utcnow()

        total_users = await session.scalar(select(func.count()).select_from(User))

        one_day_ago = now - timedelta(days=1)
        last_1_day = await session.scalar(
            select(func.count()).where(User.created_at >= one_day_ago)
        )

        seven_days_ago = now - timedelta(days=7)
        last_7_days = await session.scalar(
            select(func.count()).where(User.created_at >= seven_days_ago)
        )

        thirty_days_ago = now - timedelta(days=30)
        last_30_days = await session.scalar(
            select(func.count()).where(User.created_at >= thirty_days_ago)
        )

        return {
            "total_users": total_users,
            "last_1_day": last_1_day,
            "last_7_days": last_7_days,
            "last_30_days": last_30_days,
        }


async def check_and_update_download_limit(tg_id: int) -> bool:
    async with get_async_session() as session:
        today = date.today()
        result = await session.execute(select(User).filter_by(tg_id=tg_id))
        user: User = result.scalars().first()

        if not user:
            return False

        if user.daily_download_date == today:
            if user.daily_download_count >= daily_donwnload_count:
                return False
            user.daily_download_count += 1
        else:
            user.daily_download_date = today
            user.daily_download_count = 1

        await session.commit()
        return True


async def get_user_locale(tg_id: int) -> str:
    async with get_async_session() as session:
        result = await session.execute(select(User.language).where(User.tg_id == tg_id))
        return result.scalar_one_or_none()


async def set_user_locale(tg_id: int, locale: str):
    async with get_async_session() as session:
        await session.execute(update(User)
            .where(User.tg_id == tg_id)
            .values(language=locale)
        )
        await session.commit()


# async def main():
#     await follow_to_account(5146109604, "strv.1")
#     await follow_to_account(5146109604, "strv.2")
#     await follow_to_account(5146109604, "strv.6")
#     await follow_to_account(5389685014, "strv.1")
#     await follow_to_account(5389685014, "strv.2")
#     await follow_to_account(5389685014, "strv.4")
#
# asyncio.run(main())
#
#
# if __name__ == '__main__':
#     asyncio.run(main())
