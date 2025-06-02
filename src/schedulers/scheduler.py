from aiogram import Bot
from apscheduler.schedulers.asyncio import AsyncIOScheduler
from apscheduler.triggers.interval import IntervalTrigger
from sqlalchemy import select

from src.database.base import async_session
from src.database.models import AutoFetchStories, MonitorAccountStatus
from src.utils.func import send_stories_to_user, check_account_status_changes

scheduler = AsyncIOScheduler()


def start_scheduler(bot: Bot, story_minutes: int, status_minutes: int):

    async def auto_fetch_stories():

        async with async_session() as session:
            result = await session.execute(select(AutoFetchStories.user_id).distinct())
            tg_ids = [row[0] for row in result.fetchall()]

            for tg_id in tg_ids:
                await send_stories_to_user(bot, tg_id)

    async def monitor_account_status():

        async with async_session() as session:
            result = await session.execute(select(MonitorAccountStatus.user_id).distinct())
            tg_ids = [row[0] for row in result.fetchall()]

            for tg_id in tg_ids:
                await check_account_status_changes(bot, tg_id)

    scheduler.add_job(auto_fetch_stories, IntervalTrigger(minutes=story_minutes))
    scheduler.add_job(monitor_account_status, IntervalTrigger(minutes=status_minutes))

    scheduler.start()