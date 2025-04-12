import datetime
from datetime import timedelta, date

from sqlalchemy import and_, func, asc
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.future import select

from src.database import async_session, get_session
from src.models import User, Search, FollowAccount, Notification


async def is_user_registered(tg_id: int):
    async with get_session() as session:
        result = await session.execute(select(User).where(and_(User.tg_id == tg_id)))
        return result.scalars().first() is not None


async def add_user_to_db(tg_id: int, fullname: str, username: str):
    async with get_session() as session:
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
    async with get_session() as session:
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
    async with get_session() as session:
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


async def follow_to_account(tg_id: int, account: str):
    async with get_session() as session:

        result = await session.execute(
            select(FollowAccount)
            .where(and_(FollowAccount.user_id == tg_id))
            .order_by(asc(FollowAccount.id))
        )
        follows = result.scalars().all()

        if any(f.account == account for f in follows):
            return

        if len(follows) < 3:
            new_follow = FollowAccount(user_id=tg_id, account=account)
            session.add(new_follow)
        else:
            oldest_follow = follows[0]
            oldest_follow.account = account

        await session.commit()


async def follow_exist(tg_id: int, account: str):
    async with get_session() as session:
        result = await session.execute(
            select(FollowAccount).where(and_(
                FollowAccount.user_id == tg_id,
                FollowAccount.account == account)))

    return result.scalars().first() is not None


async def get_accounts_by_user_id(user_id: int):
    async with get_session() as session:
        stmt = select(FollowAccount.account).where(and_(FollowAccount.user_id == user_id))
        result = await session.execute(stmt)
        accounts = result.scalars().all()
        return accounts


async def notification_account(tg_id: int, account: str):
    async with get_session() as session:

        result = await session.execute(
            select(Notification)
            .where(and_(Notification.user_id == tg_id))
            .order_by(asc(Notification.id))
        )
        follows = result.scalars().all()

        if any(f.account == account for f in follows):
            return

        if len(follows) < 3:
            new_follow = Notification(user_id=tg_id, account=account)
            session.add(new_follow)
        else:
            oldest_follow = follows[0]
            oldest_follow.account = account

        await session.commit()


async def notif_exist(tg_id: int, account: str):
    async with get_session() as session:
        result = await session.execute(
            select(Notification).where(and_(
                Notification.user_id == tg_id,
                Notification.account == account)))

    return result.scalars().first() is not None


async def get_user_accounts(tg_id: int) -> list[str]:
    async with get_session() as session:
        result = await session.execute(
            select(FollowAccount.account).where(and_(FollowAccount.user_id == tg_id)))

        return [row[0] for row in result.fetchall()]


async def get_notif_acc(tg_id: int) -> list[str]:
    async with get_session() as session:
        result = await session.execute(
            select(Notification.account).where(and_(Notification.user_id == tg_id)))

        return [row[0] for row in result.fetchall()]


async def check_and_update_download_limit(tg_id: int) -> bool:
    async with get_session() as session:
        today = date.today()
        result = await session.execute(select(User).filter_by(tg_id=tg_id))
        user: User = result.scalars().first()

        if not user:
            return False

        if user.daily_download_date == today:
            if user.daily_download_count >= 3:
                return False
            user.daily_download_count += 1
        else:
            user.daily_download_date = today
            user.daily_download_count = 1

        await session.commit()
        return True


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
