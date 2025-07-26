from sqlalchemy import select, update

from src.database.base import get_async_session
from src.database.models.models import InstagramSession, InstagramAccount


async def get_session_data(account: str) ->  bytes:
    async with get_async_session() as session:
        query = select(InstagramSession.session_data
        ).where(InstagramSession.account == account
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def create_or_update_session(account: str, session_data: bytes) -> None:
    async with get_async_session() as session:
        query = select(InstagramSession
        ).where(InstagramSession.account == account
        )
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            update_query = (
                update(InstagramSession)
                .where(InstagramSession.account == account)
                .values(session_data=session_data)
            )
            await session.execute(update_query)
        else:
            new_session_data = InstagramSession(account=account, session_data=session_data)
            session.add(new_session_data)

        await session.commit()   


async def get_account(username: str) -> str:
    async with get_async_session() as session:
        query = select(InstagramAccount
        ).where(InstagramAccount.username == username
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
 

async def create_account(username: str, password: str) -> None:
    async with get_async_session() as session:
        query = InstagramAccount(
            username=username,
            password=password
        )    
        session.add(query)
        session.commit()