import asyncio
import logging
from aiogram.types import BotCommand

from src.config.config import settings
from src.bot.handlers.handlers import startup_answer, shutdown_answer
from src.config.loader import bot, dp
from src.tasks.scheduler import start_scheduler
from src.utils.login_insta import login_to_instagram
from src.utils.login_scheduler import login_to_instagram1
from src.utils.middlewere import Middleware
from src.i18n.i18n_setup import DBI18nMiddleware, i18n
from src.bot.handlers.profile import send_profile
from src.bot.handlers.stories import send_stories
from src.bot.handlers.auto_fetch import follow_list


async def main():
    logging.info("🚀  Bot ishga tushmoqda...")

    login_result = login_to_instagram(settings.INSTAGRAM_USERNAME, settings.INSTAGRAM_PASSWORD)
    logging.info(login_result)

    login_result1 = login_to_instagram1(settings.INSTAGRAM_USERNAME_SCHEDULER, settings.INSTAGRAM_PASSWORD_SCHEDULER)
    logging.info(login_result1)

    dp.startup.register(startup_answer)
    dp.shutdown.register(shutdown_answer)

    dp.message.middleware(DBI18nMiddleware(i18n=i18n))
    dp.callback_query.middleware(DBI18nMiddleware(i18n=i18n))

    dp.callback_query.middleware(Middleware())

    start_scheduler(
        bot,
        story_minutes=settings.AUTO_REFRESH_STORIES,
        status_minutes=settings.AUTO_REFRESH_STATUS_ACC
    )

    await bot.set_my_commands([
        BotCommand(command="/start", description="Qayta ishga tushirish"),
        BotCommand(command="/get", description="Hikoyalarni ko'rish"),
        BotCommand(command="/language", description="Tilni tanlang"),
        BotCommand(command="/subscription", description="Obunalarni ko'rish"),
        BotCommand(command="/chats", description="Chatlarni ko'rish"),
        BotCommand(command="/support", description="Qo'llab qo'vatlash"),
    ])

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO)
    asyncio.run(main())