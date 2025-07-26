from fastapi import Depends
from sqlalchemy import select, desc
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.models.models import (
    DeviceInfo,
    InstagramAccount,  
    InstagramSession,
)
from src.database.base import get_async_session

class LoginToInstagramRepository:
    def __init__(self, session: AsyncSession) -> None:
        self.session = session


    async def create_session(self, username: str, session_data: bytes) -> None:
        subquery = (
            select(InstagramAccount.id)
            .where(InstagramAccount.username == username)
        )
        result = await self.session.execute(subquery)
        account_id = result.scalar_one()

        query = (
            select(InstagramSession.session_data)
            .where(InstagramSession.account_id == account_id)
        )  
        result = await self.session.execute(query)
        existing = result.scalar_one_or_none()

        if not existing:
            new_session = InstagramSession(
                account_id=account_id, 
                session_data=session_data
            )
            self.session.add(new_session)
        await self.session.commit()


    async def update_session(self, account_id: int, session_data: bytes) -> None:  
        query = (
            select(InstagramSession.session_data)
            .where(InstagramSession.account_id == account_id)
        )  
        result = await self.session.execute(query)
        rows = result.scalar_one_or_none()

        if rows:
            update_session = InstagramSession(
                account_id=account_id, 
                session_data=session_data
            )
            self.session.update(update_session)
        self.session.commit()


    async def create_account(self, username: int, password: int) -> None:
        query = (
            select(InstagramAccount.username)
            .where(InstagramAccount.username == username)
        )
        result = await self.session.execute(query)
        existing = result.scalar_one_or_none()

        if not existing:
            new_account = InstagramAccount(
                username=username, 
                password=password
            )
            self.session.add(new_account)
            await self.session.commit()


    async def get_device_info(self):
        query = (
            select(DeviceInfo.device_settings)
            .order_by(desc(DeviceInfo.created_at))
            .limit(1)
        )
        result = await self.session.execute(query)
        return result.scalar_one_or_none()


# def get_login_repo() -> LoginToInstagramRepository:
#     return LoginToInstagramRepository()

def get_login_repo(
    session: AsyncSession = Depends(get_async_session)
) -> LoginToInstagramRepository:
    return LoginToInstagramRepository(session=session)