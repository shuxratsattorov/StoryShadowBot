from sqlalchemy import and_, asc, update
from sqlalchemy.future import select

from src.database.base import get_session
from database.models.models import MonitorAccountStatus


async def add_or_replace_monitored_account(tg_id: int, username: str):
    async with get_session() as session:
        result = await session.execute(
            select(MonitorAccountStatus)
            .where(and_(MonitorAccountStatus.user_id == tg_id))
            .order_by(asc(MonitorAccountStatus.id))
        )
        follows = result.scalars().all()

        if any(f.account == username for f in follows):
            return

        if len(follows) < 3:
            new_follow = MonitorAccountStatus(user_id=tg_id, account=username)
            session.add(new_follow)
        else:
            oldest_follow = follows[0]
            oldest_follow.account = username

        await session.commit()


async def is_account_monitored(tg_id: int, username: str):
    async with get_session() as session:
        result = await session.execute(
            select(MonitorAccountStatus)
            .where(and_(
                MonitorAccountStatus.user_id == tg_id,
                MonitorAccountStatus.account == username)))

    return result.scalars().first() is not None


async def get_monitored_accounts(tg_id: int) -> list[str]:
    async with get_session() as session:
        result = await session.execute(
            select(MonitorAccountStatus.account).where(and_(MonitorAccountStatus.user_id == tg_id)))

        return [row[0] for row in result.fetchall()]


async def get_last_status_acc(username: str) -> bool:
    async with get_session() as session:
        result = await session.execute(
            select(MonitorAccountStatus.was_private)
            .where(and_(MonitorAccountStatus.account == username)))

        last_status = result.scalar_one_or_none()
        return last_status


async def update_last_status_acc(username: str, status: bool):
    async with get_session() as session:
        await session.execute(
            update(MonitorAccountStatus)
            .where(and_(MonitorAccountStatus.account == username))
            .values(was_private=status)
        )
        await session.commit()