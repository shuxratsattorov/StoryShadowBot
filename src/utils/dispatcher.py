import random
from sqlalchemy.ext.asyncio import AsyncSession
from instagrapi.exceptions import LoginRequired

from client_loader import load_client
from src.database.orm.dispatcher import SmartDispatcherRepository


class SmartDispatcher:
    def __init__(self, session: AsyncSession):
        self.session = session
        self.repo = SmartDispatcherRepository()


    async def process(self):
        await self.repo.refresh_sessions()
        available_sessions = await self.repo.get_available_session()

        session_data = random.choice(available_sessions)

        try:
            cl = load_client(session_data=session_data.session_data)

        except LoginRequired:
            await self.repo.mark_invalid(account=session_data.account)

        except Exception as e:
            await self.repo.mark_invalid(account=session_data.account, error=str(e))
            raise e
