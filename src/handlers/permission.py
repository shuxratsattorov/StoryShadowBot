import os

from aiogram import Bot, Dispatcher, types
from dotenv import load_dotenv

from src.config import BOT_TOKEN
from src.keyboards.reply_keyboard import admin_reply_keyboards

load_dotenv()

ADMIN_CHAT_ID = os.getenv("ADMIN_CHAT_ID")

bot = Bot(token=BOT_TOKEN)
dp = Dispatcher()


def is_admin(user_id):
    admin_ids = {5146109604}
    return user_id in admin_ids


def load_chats():
    if ADMIN_CHAT_ID:
        chat_ids = ADMIN_CHAT_ID.strip("[]").replace('"', '').replace("'", "").split(",")
        try:
            return list(map(int, map(str.strip, chat_ids)))
        except ValueError:
            return []
    return []


def save_chats(chat_ids):
    env_path = os.path.join(os.path.dirname(__file__), "..", ".env")
    chat_ids_str = "[" + ", ".join(map(str, chat_ids)) + "]"

    lines = []
    if os.path.exists(env_path):
        with open("env_path", "r", encoding="utf-8") as f:
            lines = f.readlines()

    with open(env_path, "w", encoding="utf-8") as f:
        for line in lines:
            if not line.startswith("ADMIN_CHAT_ID = "):
                f.write(line)
        f.write(f"ADMIN_CHAT_ID = {chat_ids_str}\n")


@dp.message(lambda message: message.text == "➕ Admin qo'shish")
async def add_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda ushbu buyruqdan foydalanish uchun ruxsat yo‘q!")
        return

    chat_id_text = message.text.strip()
    try:
        chat_id = int(chat_id_text)
    except ValueError:
        await message.answer("⚠️ Iltimos, qo‘shmoqchi bo‘lgan chat ID ni kiriting:\nMisol: `5146109604`")
        return

    chat_list = load_chats()
    if chat_id in chat_list:
        await message.answer(f"⚠️ Ushbu chat ID {chat_id} allaqachon mavjud!")
        return

    chat_list.append(chat_id)
    save_chats(chat_list)
    await message.answer(f"✅ Admin {chat_id} qo‘shildi!")


@dp.message(lambda message: message.text == "🪓 Admin o'chirish")
async def delete_admin(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda ushbu buyruqdan foydalanish uchun ruxsat yo‘q!")
        return

    chat_id_text = message.text.strip()

    try:
        chat_id = int(chat_id_text)
    except ValueError:
        await message.answer("⚠️ Iltimos, o‘chirmoqchi bo‘lgan chat ID ni kiriting:\nMisol: 5146109605`")
        return

    chat_list = load_chats()
    if chat_id not in chat_list:
        await message.answer(f"⚠️ Ushbu chat ID {chat_id} ro‘yxatda yo‘q!")
        return

    chat_list.remove(chat_id)
    save_chats(chat_list)
    await message.answer(f"✅ Chat ID {chat_id} o‘chirildi!")


@dp.message(lambda message: message.text == "👤 Adminlar")
async def show_list_admin(message: types.Message):
    chat_list = load_chats()
    if not chat_list:
        await message.answer("⚠️ Adminlar ro‘yxati bo‘sh!")
        return

    result = "***Adminlar ro‘yxati:***\n"
    for idx, chat_id in enumerate(chat_list, start=1):
        result += f"{idx}. {chat_id}\n"

    await message.answer(result, parse_mode="Markdown")


@dp.message(lambda message: message.text in ["📊 Statistika", "👤 Adminlar", "➕ Admin qo'shish", "🪓 Admin o'chirish"])
async def show_admin_menu(message: types.Message):
    if not is_admin(message.from_user.id):
        await message.answer("❌ Sizda ushbu buyruqdan foydalanish uchun ruxsat yo‘q!")
        return

    await message.answer("Admin menusi:", reply_markup=admin_reply_keyboards)