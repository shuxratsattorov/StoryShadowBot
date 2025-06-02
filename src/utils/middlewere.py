from typing import Callable, Awaitable

from aiogram import BaseMiddleware
from aiogram.types import CallbackQuery

from src.orm.orm import check_and_update_download_limit


class Middleware(BaseMiddleware):
    async def __call__(self, handler: Callable[[CallbackQuery], Awaitable], callback: CallbackQuery, data: dict) -> any:
        if callback.data.startswith("view_current_stories"):
            tg_id = callback.from_user.id
            is_allowed = await check_and_update_download_limit(tg_id)
            if not is_allowed:
                await callback.message.answer(
                    "Afsuski limitga yetdingiz, limitni oshirish uchun do'stlaringizni taklif qiling!"
                )
                return
        return await handler(callback, data)