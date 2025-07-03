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

# import asyncio
# from datetime import datetime, timedelta
# from apscheduler.schedulers.asyncio import AsyncIOScheduler

# # Bu yerda containerlab o'rniga async test funksiyasi ishlatyapmiz
# async def run_containerlab(name):
#     print(f"{datetime.now().strftime('%H:%M:%S')} - {name} started")
#     await asyncio.sleep(5)  # bu yerda containerlab chaqiruvi bo'lishi mumkin
#     print(f"{datetime.now().strftime('%H:%M:%S')} - {name} finished")

# async def main():
#     scheduler = AsyncIOScheduler()

#     now = datetime.now()

#     # Uchta job, turli vaqtlar va biri parallel:
#     scheduler.add_job(run_containerlab, args=["lab1"], trigger='interval', seconds=20, start_date=now + timedelta(seconds=2))
#     scheduler.add_job(run_containerlab, args=["lab2"], trigger='interval', seconds=20, start_date=now + timedelta(seconds=4))
#     scheduler.add_job(run_containerlab, args=["lab3"], trigger='interval', seconds=20, start_date=now + timedelta(seconds=4))  # lab2 bilan bir vaqtda

#     scheduler.start()

#     print(f"{now.strftime('%H:%M:%S')} - Scheduler started. Waiting for jobs...")

#     # Event loopni to'xtatmaslik uchun
#     while True:
#         await asyncio.sleep(1)

# # Faol ishga tushirish
# if __name__ == "__main__":
#     asyncio.run(main())
