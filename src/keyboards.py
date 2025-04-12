from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

user_reply_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💌 Obunalar"),
            KeyboardButton(text=" Premium"),
        ],
        [
            KeyboardButton(text="Chatlar"),
            KeyboardButton(text="Qo'llab quvatlash"),
        ],
    ],
    resize_keyboard=True
)

admin_reply_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="📊 Statistika"),
            KeyboardButton(text="👤 Adminlar"),
        ],
        [
            KeyboardButton(text="➕ Admin qo'shish"),
            KeyboardButton(text="🪓 Admin o'chirish"),
        ]
    ],
    resize_keyboard=True
)


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


def get_profile_status_button(username: str) -> InlineKeyboardMarkup:

    profile_button = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text="👀 Joriy hikoyalarni ko'rish", callback_data=f"view_current_stories:{username}"
                )
            ],
            [
                InlineKeyboardButton(
                    text="💌 Hikoyalarga obuna olib tashlash", callback_data=f"follow_to_account:{username}"
                )
            ]
        ]
    )
    return profile_button


# async def show_admin_buttons(user_id: int):
#     admin = load_chats()
#     return user_id in admin
#
#
# async def get_keyboard(message: Message):
#     if await show_admin_buttons(message.from_user.id):
#         return admin_buttons
#     return buttons_keyboard