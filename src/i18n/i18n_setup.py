from aiogram.utils.i18n import I18n
from typing import Optional, Dict, Any
from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import SimpleI18nMiddleware

from src.orm.orm import get_user_locale, set_user_locale


class DBI18nMiddleware(SimpleI18nMiddleware):

    def __init__(
        self,
        i18n: I18n,
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user = event.from_user
        if not user:
            return await super().get_locale(event, data)

        tg_id = user.id
        locale = await get_user_locale(tg_id)

        if not locale:
            locale = await super().get_locale(event, data)
            await set_user_locale(tg_id, locale)

        return locale


i18n = I18n(path="src/i18n/locales", domain="messages")

_ = i18n.gettext
__ = i18n.lazy_gettext