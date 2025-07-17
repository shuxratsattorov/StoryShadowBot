from aiogram import Bot, Dispatcher

from src.config.config import settings

BOT_TOKEN = settings.BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()