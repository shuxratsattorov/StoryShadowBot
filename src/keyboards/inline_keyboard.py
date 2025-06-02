from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton


def get_close_profile_button(username: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔔 Akkaunt o'chilishi haqida xabar berish", callback_data=f"report_account_deletion:{username}"
                )
            ]
        ]
    )
    return keyboard


def get_profile_button(username: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Joriy hikoyalarni ko'rish", callback_data=f"view_current_stories:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💌 Hikoyalarga obuna bo'lish", callback_data=f"follow_to_account:{username}"
                )
            ]
        ]
    )
    return keyboard


def delete_profile_button(username: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Joriy hikoyalarni ko'rish", callback_data=f"view_current_stories:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💌 Obunani olib tashlash", callback_data=f"delete_to_account:{username}"
                )
            ]
        ]
    )
    return keyboard


def private_profile_button(username: str) -> InlineKeyboardMarkup:

    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="🔔 Akkaunt o'chilishi haqida xabar berish", callback_data=f"report_account_deletion:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💌 Obunani olib tashlash", callback_data=f"delete_to_account:{username}"
                )
            ]
        ]
    )
    return keyboard


def share_to_chat() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Botni guruhga taklif qiling", url="https://t.me/storyshadowbot?startgroup=true"
                )
            ]
        ]
    )
    return keyboard


def share_to_friends() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Ulashish", url="https://t.me/share/url?url=https://t.me/storyninjabot?start=u5146109604&text="
                )
            ]
        ]
    )
    return keyboard


def support_button() -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="Bizga yozing", url="https://t.me/yspvc"
                )
            ]
        ]
    )
    return keyboard


def select_language(username) -> InlineKeyboardMarkup:
    keyboard = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="uz", callback_data=f"uz:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="ru", callback_data=f"ru:{username}"
                )
            ]
        ]
    )
    return keyboard

# async def show_admin_buttons(user_id: int):
#     admin = load_chats()
#     return user_id in admin
#
#
# async def get_keyboard(message: Message):
#     if await show_admin_buttons(message.from_user.id):
#         return admin_buttons
#     return buttons_keyboard