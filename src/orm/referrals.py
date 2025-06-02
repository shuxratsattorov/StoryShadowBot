from sqlalchemy import and_
from sqlalchemy.future import select

from src.database.base import get_session
from src.database.models import Referral


async def referral(tg_id: int, refer_user):
    async with get_session() as session:
        result = await session.execute(select(Referral).where(and_(Referral.user_id == tg_id)))
        refer = result.scalars.first()

        if not refer:
            new_refer = Referral(
                user_id=tg_id,
                referred_user=refer_user
            )
            session.add(new_refer)
            await session.commit()