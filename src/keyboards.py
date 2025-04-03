from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton, Message
from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.handlers.permission_handler import load_chats

# buttons_keyboard = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="Istoriya korish"),
#         ],
# [
#             KeyboardButton(text="Chat"),
#             KeyboardButton(text="Qullab quvatlash"),
#         ],
#     ],
#     resize_keyboard=True
# )
#
# admin_buttons = ReplyKeyboardMarkup(
#     keyboard=[
#         [
#             KeyboardButton(text="🔒 Bloklash"),
#             KeyboardButton(text="🔓 Blokdan ochish"),
#         ],
#         [
#             KeyboardButton(text="👤 Admin"),
#             KeyboardButton(text="📊 Statistika"),
#         ]
#     ]
# )
#
#
# inline_keyboard = InlineKeyboardMarkup(
#     keyboard=[
#         [
#             InlineKeyboardButton(text="Huquq berish"),
#             InlineKeyboardButton(text="Huquq olish"),
#         ]
#     ]
# )

profile_button = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="Joriy hikoyalarni ko'rish", callback_data="view_current_stories"
            )
        ]
    ]
)


# async def show_admin_buttons(user_id: int):
#     admin = load_chats()
#     return user_id in admin
#
#
# async def get_keyboard(message: Message):
#     if await show_admin_buttons(message.from_user.id):
#         return admin_buttons
#     return buttons_keyboard