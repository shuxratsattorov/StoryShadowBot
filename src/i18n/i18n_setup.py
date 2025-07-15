from aiogram.utils.i18n import I18n
from typing import Optional, Dict, Any
from aiogram.types import TelegramObject
from aiogram.utils.i18n.middleware import I18nMiddleware

from src.database.orm.orm import get_user_locale


class DBI18nMiddleware(I18nMiddleware):

    def __init__(
        self,
        i18n: I18n,
        i18n_key: Optional[str] = "i18n",
        middleware_key: str = "i18n_middleware",
    ) -> None:
        super().__init__(i18n=i18n, i18n_key=i18n_key, middleware_key=middleware_key)

    async def get_locale(self, event: TelegramObject, data: Dict[str, Any]) -> str:
        user = event.from_user

        locale = await get_user_locale(user.id)
        if locale:
            return locale

        if user.language_code:
            return user.language_code

        return self.i18n.default_locale


i18n = I18n(path="src/i18n/locales", default_locale="ru", domain="messages")

_ = i18n.gettext
__ = i18n.lazy_gettext