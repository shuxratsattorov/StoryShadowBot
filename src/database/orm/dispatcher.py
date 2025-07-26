from typing import Optional
from sqlalchemy import select
from datetime import datetime, timedelta
from sqlalchemy.ext.asyncio import AsyncSession

from src.database.base import get_async_session
from src.database.models.models import InstagramSession


class SmartDispatcherRepository:
    def __init__(self):
        self.session: AsyncSession = get_async_session()
        self.db = InstagramSession
        self.now = datetime.utcnow()


    async def get_available_session(self) -> bytes:
        query = (
            select(self.db.session_data)
            .where(self.db.is_active == True,
                   self.db.is_valid == True,
                   self.db.is_on_cooldown == False)
        )
        result = await self.session.execute(query)
        return result.scalars().all() 


    async def refresh_sessions(self) -> None:
        query = (
            select(self.db)
            .where(self.db.is_on_cooldown == True)
        ) 
        result = await self.session.execute(query)
        rows = result.scalars().all()

        for row in rows:
            if row.cooldown_until <= self.now:
                row.cooldown_until = False
                row.cooldown_until = None
                row.last_error = None
                self.session.update(row)
        self.session.commit()  


    async def apply_cooldown(self, account: str, minutes: int = 5) -> None:
        query = (
            select(self.db)
            .where(self.db.account == account)
        )
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()

        if not row.last_used_at or row.last_used_at.date() != self.now.date():
            row.daily_usage_count = 0

        row.usage_count += 1
        row.daily_usage_count += 1
        row.is_on_cooldown = True
        row.cooldown_until = self.now + timedelta(minutes=minutes)
        row.last_used_at = self.now

        await self.session.commit()


    async def mark_invalid(self, account: str, error: Optional[str] = None) -> None:
        query = (
            select(self.db)
            .where(self.db.account == account)
        )
        result = await self.session.execute(query)
        row = result.scalar_one_or_none()

        row.is_valid = False
        row.last_error = str(error)[:255] if error else "Unknown error"
        
        await self.session.commit()
