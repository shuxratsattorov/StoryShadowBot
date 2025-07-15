from sqlalchemy import select, update
from src.database.models.models import InstagramSession, InstaramAccount


async def get_session(account: str) ->  bytes:
    async with get_session() as session:
        query = select(InstagramSession.session
        ).where(InstagramSession.account == account
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()


async def create_or_update_session(account: str, session: bytes) -> None:
    async with get_session() as session:
        query = select(InstagramSession
        ).where(InstagramSession.account == account
        )
        result = await session.execute(query)
        existing = result.scalar_one_or_none()

        if existing:
            update_query = (
                update(InstagramSession)
                .where(InstagramSession.account == account)
                .values(session=session)
            )
            await session.execute(update_query)
        else:
            new_session = InstagramSession(account=account, session=session)
            session.add(new_session)


async def get_account(username: str) -> str:
    async with get_session() as session:
        query = select(InstaramAccount
        ).where(InstaramAccount.username == username
        )
        result = await session.execute(query)
        return result.scalar_one_or_none()
 

async def create_account(username: str, password: str) -> None:
    async with get_session() as session:
        query = InstaramAccount(
            username=username,
            password=password
        )    
        session.add(query)
        session.commit()