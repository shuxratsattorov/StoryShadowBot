from aiogram import Bot, Dispatcher

from src.config.config import BOT_TOKEN

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()