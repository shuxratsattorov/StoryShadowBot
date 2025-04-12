import os
import re
from datetime import datetime, timedelta

import requests
from aiogram import Bot, Dispatcher, F
from aiogram.filters import Command
from aiogram.types import Message, FSInputFile, CallbackQuery
from instagrapi.exceptions import UserNotFound
from sqlalchemy.ext.asyncio import AsyncSession

from src.config import CHAT_ID
from src.keyboards import get_profile_button, get_close_profile_button
from src.login_instagram import cl
from src.orm import add_user_to_db, save_search_to_db, is_user_registered, follow_to_account, follow_exist, \
    check_and_update_download_limit

dp = Dispatcher()
log_chat_id = 'CHAT_ID'


async def startup_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishga tushdi! ✅")


async def shutdown_answer(bot: Bot):
    await bot.send_message(CHAT_ID, "Bot ishdan to'xtadi! ❌")


@dp.message(Command("start"))
async def start(message: Message, bot: Bot):
    user_exists = await is_user_registered(message.from_user.id)

    if not user_exists:
        await add_user_to_db(
            tg_id=message.from_user.id,
            fullname=message.from_user.full_name,
            username=message.from_user.username,
        )
        await bot.send_message(CHAT_ID, "✅ Yangi foydalanuvchi ro'yxatdan otdi!")

    await message.answer(f"Salom, men Insta Shadow - sizning shaxsiy Instagram kuzatuvchingiz.\n"
                         f"Men sizga hikoyalari anonim ravishda kuzatishga yordam beraman.\n"
                         f"Sizni qiziqtirgan kishining foydalanuvchi nomi yoki instagram havolasini yuboring.")


@dp.message()
async def send_profile(message: Message, bot: Bot, save_path="users_media/"):

    username_or_url = message.text.strip()

    if username_or_url.startswith("@"):
        username = username_or_url[1:]
    else:
        match = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", username_or_url)
        username = match.group(1).split("?")[0] if match else username_or_url

    wait_msg = await message.answer("⌛️")

    try:
        user_info = cl.user_info_by_username(username)
        profile_pic_url = user_info.profile_pic_url_hd
        account_status = f"`@{username}` - Yopiq akkaunt." if user_info.is_private else f"`@{username}`"

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

            if user_info.is_private:
                profile_button = get_close_profile_button(username)
            else:
                profile_button = get_profile_button(username)

            await bot.send_photo(
                message.chat.id,
                FSInputFile(file_name),
                caption=account_status,
                parse_mode="Markdown",
                reply_markup=profile_button
            )
            os.remove(file_name)

    except UserNotFound:
        await message.answer(f"`@{username}` profili topilmadi.", parse_mode="Markdown")

    except Exception as e:
        await message.answer(f"❌ Xatolik yuz berdi")
        await bot.send_message(log_chat_id, f"❌ Xatolik yuz berdi: {e}")

    await bot.delete_message(message.chat.id, wait_msg.message_id)


@dp.callback_query(F.data.startswith("view_current_stories"))
async def send_stories(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    tg_id = callback.from_user.id

    if not await check_and_update_download_limit(tg_id):
        await callback.message.answer(f"Afsuski limitga yetdingiz, limitni oshirish uchun do'stlaringzni taklif qiling!", parse_mode="Markdown")
        return

    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)

        if not stories:
            await callback.message.answer(f"`@{username}` profilida hozircha hech qanday hikoyalar mavjud emas.", parse_mode="Markdown")
        else:
            await callback.message.answer(f"Yuklanmoqda {len(stories)} hikoyalar `@{username}`",  parse_mode="Markdown")

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

                    mentions = ' '.join([f"@{mention.user.username}" for mention in story.mentions]) if story.mentions else ''

                    uzb_time = datetime.utcfromtimestamp(story.taken_at.timestamp()) + timedelta(hours=5)
                    story_time = uzb_time.strftime("%d.%m.%Y, %H:%M:%S UZB")
                    caption_text = (
                        f"`@{username}` hikoyasi ({index + 1}/{len(stories)})\n\n"
                    )

                    if mentions:
                        caption_text += f"Metka: `{mentions}`\n\n"

                    caption_text += f"{story_time}"

                    if story.video_url:
                        await callback.message.answer_video(FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")
                    else:
                        await callback.message.answer_photo(FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")

                    os.remove(file_name)
                else:
                    await callback.message.answer("Yuklab olishda xatolik yuz berdi.")

            except Exception as e:
                await callback.message.answer(f"❌ {index + 1}-hikoyani yuklashda xatolik")
                await callback.bot.send_message(log_chat_id, f"❌ {index + 1}-hikoyani yuklashda xatolik: {e}")

    except Exception as e:
        await callback.message.answer(f"❌ Xatolik yuz berdi")
        await callback.bot.send_message(log_chat_id, f"❌ Xatolik yuz berdi: {e}")


@dp.callback_query(F.data.startswith("follow_to_account"))
async def follow_to_accounts(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    account_exist = await follow_exist(tg_id=user_id, account=username)

    if not account_exist:
        await follow_to_account(tg_id=user_id, account=username)
        await callback.message.answer(f"Siz `@{username}` ga obuna bo'ldingiz! End men sizga hikoyalar qoyishi bilan yuklab beraman.", parse_mode="Markdown")
    else:
        await callback.message.answer("Siz allaqachon obuna bo'lgansiz")


@dp.callback_query(F.data.startswith("report_account_deletion"))
async def notification_open_account(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    account_exist = await follow_exist(tg_id=user_id, account=username)

    if not account_exist:
        await follow_to_account(tg_id=user_id, account=username)
        await callback.message.answer(f"Sizga `@{username}` account ochilganda albatta xabar beraman!", parse_mode="Markdown")
    else:
        await callback.message.answer("Siz allaqachon obuna bo'lgansiz!")
