import os
import re
from datetime import datetime

import requests
from aiogram import Bot, Dispatcher
from aiogram import Router, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from instagrapi.exceptions import UserNotFound

from src.config import CHAT_ID
from src.instagram_api import cl
from src.keyboards import profile_button
from src.orm import add_user_to_db, save_search_to_db

dp = Dispatcher()
router = Router()


async def startup_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishga tushdi! ✅")


async def shutdown_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishdan to'xtadi! ❌")


@dp.message(Command("start"))
async def start(message: Message, bot: Bot):
    await add_user_to_db(
        tg_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
    )
    await message.answer(f"Salom, men InstaShadow - sizning shaxsiy Instagram kuzatuvchingiz.\n"
                         f"Men sizga boshqa odamlarning hikoyalari anonim ravishda kuzatishga yordam beraman.\n"
                         f"Sizni qiziqtirgan kishining foydalanuvchi nomi yoki Instagram havolasini yuboring.")

    await bot.send_message(CHAT_ID, "✅ Yangi foydalanuvchi ro'yxatdan otdi!")


@dp.message()
async def send_profile(message: Message, bot: Bot, save_path="users_media/"):

    username_or_url = message.text.strip()

    match = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", username_or_url)
    username = match.group(1).split("?")[0] if match else username_or_url
    wait_msg = await message.answer("⌛️")

    try:
        user_info = cl.user_info_by_username(username)
        profile_pic_url = user_info.profile_pic_url_hd
        account_status = " - Yopiq akkaunt." if user_info.is_private else ""

        if profile_pic_url:
            await save_search_to_db(
                tg_id=message.from_user.id,
                search_query=username
            )

        os.makedirs(save_path, exist_ok=True)

        file_name = os.path.join(save_path, f"{username}_profile.jpg")
        response = requests.get(profile_pic_url, stream=True)

        if response.status_code == 200:
            with open(file_name, "wb") as file:
                for chunk in response.iter_content(1024):
                    file.write(chunk)

            await bot.send_photo(
                message.chat.id,
                FSInputFile(file_name),
                caption=f"`@{username}`{account_status}",
                parse_mode="Markdown",
                reply_markup=profile_button
            )

    except UserNotFound:
        await message.answer(f"`@{username}` profili topilmadi. Yozuv to'g'riligini tekshiring va qaytadan urinib ko'ring.", parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi: {e}")

    await bot.delete_message(message.chat.id, wait_msg.message_id)


@router.callback_query(F.data == "view_current_stories")
async def send_stories(callback: CallbackQuery):
    username = callback.from_user.username
    await callback.answer("Hikoyalarni yuklab olish boshlandi...")

    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)

        if not stories:
            await callback.message.answer(f"`@{username}` profilida hozircha hech qanday hikoyalar yo‘q.", parse_mode="Markdown")
            return

        save_path = "stories_media/"
        os.makedirs(save_path, exist_ok=True)

        for index, story in enumerate(stories):
            try:
                media_url = story.video_url or story.thumbnail_url
                file_extension = ".mp4" if story.video_url else ".jpg"
                file_name = os.path.join(save_path, f"{username}_story_{index + 1}{file_extension}")

                response = requests.get(media_url, stream=True)

                if response.status_code == 200:
                    with open(file_name, "wb") as file:
                        for chunk in response.iter_content(1024):
                            file.write(chunk)

                    story_time = datetime.utcfromtimestamp(story.taken_at.timestamp()).strftime("%d.%m.%Y, %H:%M:%S UZB")
                    caption_text = f"`@{username}` hikoyasi ({index + 1}/{len(stories)})\n\n📅 {story_time}"

                    if story.video_url:
                        await callback.message.answer_video(FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")
                    else:
                        await callback.message.answer_photo(FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")

                    os.remove(file_name)
                else:
                    await callback.message.answer("Yuklab olishda xatolik yuz berdi.")

            except Exception as e:
                await callback.message.answer(f"❌ {index + 1}-hikoyani yuklashda xatolik: {e}")

    except Exception as e:
        await callback.message.answer(f"❌ Xatolik yuz berdi: {e}")