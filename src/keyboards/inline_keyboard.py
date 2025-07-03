from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from src.i18n.i18n_setup import i18n

__ = i18n.gettext


def get_close_profile_button(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("🔔 Уведомить меня об открытии аккаунта"), callback_data=f"report_account_deletion:{username}"
                )
            ]
        ]
    )


def get_profile_button(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("👀 Посмотреть текущие истории"), callback_data=f"view_current_stories:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=__("💌 Подписаться на истории"), callback_data=f"follow_to_account:{username}"
                )
            ]
        ]
    )


def delete_profile_button(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("👀 Посмотреть текущие истории"), callback_data=f"view_current_stories:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=__("💌 Подписаться на истории"), callback_data=f"delete_to_account:{username}"
                )
            ]
        ]
    )


def private_profile_button(username: str) -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("🔔 Уведомить меня об открытии аккаунта"), callback_data=f"report_account_deletion:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text=__("💌 Отписаться на истории"), callback_data=f"delete_to_account:{username}"
                )
            ]
        ]
    )


def share_to_chat() -> InlineKeyboardMarkup:
    _ = i18n.gettext
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("Пригласить бота в чат"), url="https://t.me/storyshadowbot?startgroup=true"
                )
            ]
        ]
    )


def share_to_friends() -> InlineKeyboardMarkup:
    _ = i18n.gettext
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=__("Поделиться"), url="https://t.me/share/url?url=https://t.me/storyninjabot?start=u5146109604&text="
                )
            ]
        ]
    )


def support_button() -> InlineKeyboardMarkup:
    _ = i18n.gettext
    return InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(text=__("✍ Написать нам"), url="https://t.me/yspvc")
            ]
        ]
    )


def select_language():
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="🇺🇿 O‘z", callback_data="lang_uz"),
            InlineKeyboardButton(text="🇷🇺 Ру", callback_data="lang_ru"),
        ]
    ])


# async def show_admin_buttons(user_id: int):
#     admin = load_chats()
#     return user_id in admin
#
#
# async def get_keyboard(message: Message):
#     if await show_admin_buttons(message.from_user.id):
#         return admin_buttons
#     return buttons_keyboard