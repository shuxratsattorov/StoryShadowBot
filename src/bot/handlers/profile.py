import os
import re
import string
import requests
from aiogram import Bot, F
from aiogram.types import FSInputFile
from instagrapi.exceptions import UserNotFound
from aiogram.types import Message, CallbackQuery

from src.config.loader import dp
from src.config.config import CHAT_ID
from src.utils.login_insta import cl
from src.database.orm.orm import save_search_to_db
from src.database.orm.auto_fetch_stories import add_or_replace_autofetch_account
from src.database.orm.monitor_acc_status import is_account_monitored, add_or_replace_monitored_account
from src.bot.keyboards.inline_keyboard import get_profile_button, get_close_profile_button, delete_profile_button


@dp.message()
async def send_profile(message: Message, bot: Bot, save_path="media/users_media/"):
    username_or_url = message.text.strip()

    if username_or_url.startswith("@"):
        username = username_or_url[1:]
    else:
        match = re.search(r"instagram\.com/([a-zA-Z0-9_.]+)", username_or_url)
        username = match.group(1).split("?")[0] if match else username_or_url

    allowed_chars = string.ascii_letters + string.digits + "._"
    if (
            len(username) > 30 or
            ".." in username or
            any(char not in allowed_chars for char in username)
    ):
        await message.answer(f"So‘rovingizni ko‘rib chiqa olmayapman.\n"
                             f"Buyruqlar roʻyxatini koʻrish uchun /help "
                             f"tugmasini bosing yoki biz bilan bogʻlanish uchun"
                             f" /support tugmasini bosing.")
        return

    wait_msg = await message.answer("⌛️")

    try:
        user_info = cl.user_info_by_username(username, use_cache=False)
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
                is_followed = await add_or_replace_autofetch_account(message.from_user.id, username)

                if is_followed:
                    profile_button = delete_profile_button(username)
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
        await bot.send_message(CHAT_ID, f"❌ Xatolik yuz berdi: {e}")

    await bot.delete_message(message.chat.id, wait_msg.message_id)


@dp.callback_query(F.data.startswith("report_account_deletion"))
async def follow_to_accounts(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    account_exist = await is_account_monitored(tg_id=user_id, username=username)

    if not account_exist:
        await add_or_replace_monitored_account(tg_id=user_id, username=username)
        await callback.message.answer(f"Sizga `@{username}` account ochilganda albatta xabar beraman!",
                                      parse_mode="Markdown")
    else:
        await callback.message.answer(f"Sizga `@{username}` account ochilganda albatta xabar beraman!",
                                      parse_mode="Markdown")