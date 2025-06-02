import os

import requests
from aiogram import Bot, F
from aiogram.filters import Command
from aiogram.types import FSInputFile
from aiogram.types import Message, CallbackQuery

from src.config import CHAT_ID
from src.keyboards.inline_keyboard import delete_profile_button
from src.keyboards.inline_keyboard import private_profile_button
from src.loader import dp
from src.orm.auto_fetch_stories import add_or_replace_autofetch_account
from src.orm.auto_fetch_stories import get_autofetch_accounts
from src.orm.auto_fetch_stories import remove_follow
from src.utils.login_insta import cl


@dp.callback_query(F.data.startswith("follow_to_account"))
async def follow_to_accounts(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    success = await add_or_replace_autofetch_account(tg_id=user_id, account=username)
    if success:
        await callback.message.answer(f"Siz `@{username}` ga obuna bo'ldingiz! "
                                      f"End men sizga hikoyalar qoyishi bilan yuklab beraman",
                                      parse_mode="Markdown")
    else:
        await callback.message.answer(f"Hikoyalarga obuna bo'lish imkoniyati limitiga yetdi, "
                                      f"iltimos **obunalar** /subscription bo'limidan tekshirin", parse_mode="Markdown")


@dp.callback_query(F.data.startswith("delete_to_account"))
async def remove_to_follow(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    await remove_follow(tg_id=user_id, account=username)
    await callback.message.answer(f"`@{username}` muvaffaqiyatli o'chirildi",
                                  parse_mode="Markdown")


@dp.message(Command("subscription"))
async def follow_list(message: Message, bot: Bot, tg_id: int, save_path="media/users_media/"):
    account = await get_autofetch_accounts(tg_id)

    for username in account:
        try:
            user_info = cl.user_info_by_username(username, use_cache=False)
            account_status = f"`@{username}` - Yopiq akkaunt." if user_info.is_private else f"`@{username}`"
            if user_info.is_private:
                profile_button = private_profile_button(username)
            else:
                profile_button = delete_profile_button(username)

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