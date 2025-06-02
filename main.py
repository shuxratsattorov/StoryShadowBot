import asyncio
import logging

from aiogram.types import BotCommand

from src.config import (
    INSTAGRAM_USERNAME,
    INSTAGRAM_PASSWORD,
    INSTAGRAM_USERNAME_SCHEDULER,
    INSTAGRAM_PASSWORD_SCHEDULER,
    AUTO_REFRESH_STORIES,
    AUTO_REFRESH_STATUS_ACC
)
from src.handlers.handlers import startup_answer, shutdown_answer
from src.loader import bot, dp
from src.schedulers.scheduler import start_scheduler
from src.utils.login_insta import login_to_instagram
from src.utils.login_scheduler import login_to_instagram1
from src.utils.middlewere import Middleware
from src.handlers.handlers import start
from src.handlers.profile import send_profile
from src.handlers.stories import send_stories
from src.handlers.auto_fetch import follow_list


async def main():
    logging.info("🚀  Bot ishga tushmoqda...")

    login_result = login_to_instagram(INSTAGRAM_USERNAME, INSTAGRAM_PASSWORD)
    logging.info(login_result)

    login_result1 = login_to_instagram1(INSTAGRAM_USERNAME_SCHEDULER, INSTAGRAM_PASSWORD_SCHEDULER)
    logging.info(login_result1)

    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)

    dp.callback_query.middleware(Middleware())

    start_scheduler(bot, story_minutes=AUTO_REFRESH_STORIES, status_minutes=AUTO_REFRESH_STATUS_ACC)

    await bot.set_my_commands([
        BotCommand(command="/start", description="Qayta ishga tushirish"),
        BotCommand(command="/get", description="Hikoyalarni ko'rish"),
        BotCommand(command="/subscription", description="Obunalarni ko'rish"),
        BotCommand(command="/chats", description="Chatlarni ko'rish"),
        BotCommand(command="/support", description="Qo'llab qo'vatlash"),
    ])

    await dp.start_polling(bot)

if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)

    asyncio.run(main())