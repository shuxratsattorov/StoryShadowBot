import datetime
from datetime import timedelta

from sqlalchemy import and_, func
from sqlalchemy.future import select

from src.database import async_session
from src.models import User, Search


async def add_user_to_db(tg_id: int, fullname: str, username: str):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(and_(User.tg_id == tg_id)))
            user = result.scalars().first()

            if not user:
                new_user = User(
                    tg_id=tg_id,
                    fullname=fullname,
                    username=username,
                )
                session.add(new_user)
                await session.commit()


async def save_search_to_db(tg_id: int, search_query: str):
    async with async_session() as session:
        async with session.begin():
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


async def block_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(and_(User.tg_id == tg_id)))
            user = result.scalars().first()

            if user:
                if user.banned:
                    user.banned = False
                    await session.commit()
                    return f"Ushbu {user.tg_id} foydalanuvchi bloklandi!"
                else:
                    return f"Ushbu {user.tg_id} foydalanuvchi allaqachon bloklangan!"
            else:
                return f"Foydalanuvchi topilmadi."


async def unblock_user(tg_id: int):
    async with async_session() as session:
        async with session.begin():
            result = await session.execute(select(User).where(and_(User.tg_id == tg_id)))
            user = result.scalars().first()

            if user:
                if user.banned:
                    user.banned = False
                    await session.commit()
                    return f"Ushbu {user.tg_id} foydalanuvchi blokdan chiqarildi!"
                else:
                    return f"Ushbu {user.tg_id} foydalanuvchi bloklanmagan!"
            else:
                return f"Foydalanuvchi topilmadi."


async def get_user_statistics():
    async with async_session() as session:
        async with session.begin():
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