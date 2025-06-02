from aiogram.types import ReplyKeyboardMarkup, KeyboardButton


user_reply_keyboards = ReplyKeyboardMarkup(
    keyboard=[
        [
            KeyboardButton(text="💌 Obunalar"),
            KeyboardButton(text="⚡️ Til"),
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