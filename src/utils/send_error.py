import inspect
import traceback
from aiogram import Bot

from src.config.config import settings

chat_id = settings.CHAT_ID


async def send_error_to_admin(bot: Bot, error: Exception):
    try:
        tb = traceback.format_exc()
        current_frame = inspect.currentframe()
        caller_frame = current_frame.f_back
        func_name = caller_frame.f_code.co_name

        message = (
            f"📌 Funksiya: `{func_name}`\n"
            f"❗️ Xatolik: ```\n{str(error)}\n```\n"
            f"🧵 Traceback:\n```{tb}```"
        )

        await bot.send_message(chat_id, message, parse_mode="Markdown")
    except Exception:
        pass 