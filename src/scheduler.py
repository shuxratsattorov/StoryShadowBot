from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from sqlalchemy import select

from src.database import async_session
from src.func import send_stories_to_user
from src.models import FollowAccount

scheduler = AsyncIOScheduler()


def start_scheduler(bot: Bot):
    @scheduler.scheduled_job("interval", minutes=5)
    async def auto_fetch_stories():
        async with async_session() as session:
            result = await session.execute(select(FollowAccount.user_id).distinct())
            tg_ids = [row[0] for row in result.fetchall()]

            for tg_id in tg_ids:
                await send_stories_to_user(bot, session, tg_id)

    @scheduler.scheduled_job("interval", minutes=10)
    async def monitor_account_status():
        async with async_session() as session:
            result = await session.execute(select(FollowAccount.account, FollowAccount.user_id).distinct())
            accounts = result.fetchall()

            for account, tg_id in accounts:
                status = await check_account_status(account)
                if status == "private":
                    await bot.send_message(tg_id, f"⚠️ `@{account}` akkaunti yopilgan.", parse_mode="Markdown")

    scheduler.start()