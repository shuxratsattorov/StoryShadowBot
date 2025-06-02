import os

import requests
from aiogram import Bot
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.types import Message

from src.config import CHAT_ID
from src.keyboards.inline_keyboard import delete_profile_button
from src.keyboards.inline_keyboard import private_profile_button
from src.keyboards.inline_keyboard import support_button, share_to_chat
from src.loader import dp
from src.orm.auto_fetch_stories import get_autofetch_accounts
from src.orm.orm import add_user
from src.utils.login_insta import cl


async def startup_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishga tushdi! ✅")


async def shutdown_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishdan to'xtadi! ❌")


@dp.message(Command("start"))
async def start(message: Message, bot: Bot):
    user_added = await add_user(
        tg_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
    )

    if user_added:
        await bot.send_message(CHAT_ID, "✅ Yangi foydalanuvchi ro'yxatdan otdi!")

    await message.answer(f"Salom, men Insta Shadow - sizning shaxsiy Instagram kuzatuvchingiz.\n"
                         f"Men sizga hikoyalari anonim ravishda kuzatishga yordam beraman.\n"
                         f"Sizni qiziqtirgan kishining foydalanuvchi nomi yoki instagram havolasini yuboring.")


@dp.message(Command("get"))
async def get(message: Message):
    await message.answer(f"Sizni qiziqtirgan shaxsning foydalanuvchi nomi yoki Instagram havolasini yuboring")


@dp.message(Command("chats"))
async def chat(message: Message):
    await message.answer(f"Agar hikoyalar va postlarni avtomatik tarzda chatga joylashtirmoqchi bo‘lsangiz, "
                         f"@storyshadowbot botini chatga qo‘shing.\n"
                         f"Faqatgina chat egasi qaysi postlar e’lon qilinishini tanlashi mumkin.\n\n"
                         f"Chatlar ro‘yxati:", reply_markup=share_to_chat())


@dp.message(Command("support"))
async def support(message: Message):
    await message.answer(f"Biz bilan bog'laning\n", reply_markup=support_button())


@dp.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(f"Kerakli kamandalar:\n\n"
                         f"/start — Qayta ishga tushirish\n"
                         f"/get — Hikoyalarni ko'rish\n"
                         f"/subscription — Obunalarni ko'rish\n"
                         f"/chats — Chatlarni ko'rish\n"
                         f"/support — Qo'llab qo'vatlash\n")


@dp.message(Command("subscription"))
async def follow_list(message: Message, bot: Bot, save_path="media/users_media/"):
    tg_id = message.from_user.id
    account = await get_autofetch_accounts(tg_id)

    wait_msg = await message.answer("⌛️")

    for username in account:
        try:
            user_info = cl.user_info_by_username(username, use_cache=False)
            is_private = user_info.is_private
            account_status = f"`@{username}` - Yopiq akkaunt." if is_private else f"`@{username}`"
            profile_button = private_profile_button(username) if is_private else delete_profile_button(username)

            os.makedirs(save_path, exist_ok=True)

            profile_pic_url = user_info.profile_pic_url_hd
            file_name = os.path.join(save_path, f"{username}_profile.jpg")
            response = requests.get(profile_pic_url, stream=True)

            if response.status_code == 200:
                with open(file_name, "wb") as file:
                    for chunk in response.iter_content(1024):
                        file.write(chunk)

                await bot.send_photo(
                    message.chat.id,
                    FSInputFile(file_name),
                    caption=account_status,
                    parse_mode="Markdown",
                    reply_markup=profile_button
                )
                os.remove(file_name)

        except Exception as e:
            await bot.send_message(CHAT_ID, f"Bo'lim: Auto Fetch Stories\nUser: {tg_id}\nXatolik: {e}")

    await bot.delete_message(message.chat.id, wait_msg.message_id)