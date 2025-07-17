import os
import requests
from aiogram import Bot
from datetime import datetime
from aiogram.types import FSInputFile

from src.config.config import settings
from instagrapi.exceptions import LoginRequired
from src.utils.login_scheduler import cl, login_to_instagram1
from src.bot.keyboards.inline_keyboard import get_profile_button
from src.database.orm.auto_fetch_stories import (
    get_autofetch_accounts, 
    get_last_story_time, 
    update_last_story_time
    )
from src.database.orm.monitor_acc_status import (
    get_monitored_accounts, 
    get_last_status_acc, 
    update_last_status_acc
    )


chat_id = settings.CHAT_ID
username = settings.INSTAGRAM_USERNAME_SCHEDULER
password = settings.INSTAGRAM_PASSWORD_SCHEDULER


async def check_account_status_changes(bot: Bot, tg_id: int, save_path="media/users_media/"):
    accounts = await get_monitored_accounts(tg_id)

    for username in accounts:
        try:
            user_info = cl.user_info_by_username(username, use_cache=False)
            current_status = user_info.is_private

            last_status = await get_last_status_acc(username)

            if last_status is not None and last_status != current_status:
                if not current_status:
                    profile_pic_url = user_info.profile_pic_url_hd
                    os.makedirs(save_path, exist_ok=True)
                    file_name = os.path.join(save_path, f"{username}_profile.jpg")
                    response = requests.get(profile_pic_url, stream=True)

                    if response.status_code == 200:
                        with open(file_name, "wb") as file:
                            for chunk in response.iter_content(1024):
                                file.write(chunk)

                        profile_button = get_profile_button(username)

                        await bot.send_photo(
                            tg_id,
                            FSInputFile(file_name),
                            caption=f"`@{username}`",
                            parse_mode="Markdown",
                            reply_markup=profile_button
                        )
                        await bot.send_message(tg_id, f"✅ Akkaunti endi ommaviy holatga o‘tdi.")

                        os.remove(file_name)

                await update_last_status_acc(username, current_status)

        except Exception as e:
            await bot.send_message(chat_id, f"Bo'lim: Monitor Account Status\nUser: {tg_id}\nXatolik: {e}")


async def send_stories_to_user(bot: Bot, tg_id: int, save_path="media/stories_media/"):
    accounts = await get_autofetch_accounts(tg_id=tg_id)

    for username in accounts:
        try:
            try:
                user_id = cl.user_id_from_username(username)
                stories = cl.user_stories(user_id)
            except LoginRequired:
                # Sessiya yaroqsiz, yangilaymiz va qayta urinib ko'ramiz
                result = login_to_instagram1(username, password)
                await bot.send_message(tg_id, f"♻️ Sessiya yangilandi: {result}")

                try:
                    user_id = cl.user_id_from_username(username)
                    stories = cl.user_stories(user_id)
                except Exception as e:
                    await bot.send_message(chat_id, f"Bo'lim: Auto Fetch Stories\nUser: {tg_id}\nSessiyadan keyin ham xatolik: {e}")
                    continue  # bu userni tashlab ketadi

            if stories:
                os.makedirs(save_path, exist_ok=True)
                last_story_time = await get_last_story_time(tg_id=tg_id, username=username)

                for index, story in enumerate(stories):
                    try:
                        time = datetime.utcfromtimestamp(story.taken_at.timestamp())

                        if time <= last_story_time:
                            continue

                        media_url = story.video_url or story.thumbnail_url
                        file_extension = ".mp4" if story.video_url else ".jpg"
                        file_name = os.path.join(save_path, f"{username}_story_{index + 1}{file_extension}")

                        response = requests.get(media_url, stream=True)

                        if response.status_code == 200:
                            with open(file_name, "wb") as file:
                                for chunk in response.iter_content(1024):
                                    file.write(chunk)

                            mentions = ' '.join([f"@{mention.user.username}" for mention in story.mentions]) if story.mentions else ''
                            story_time = time.strftime("%d.%m.%Y, %H:%M:%S UZB")
                            caption_text = f"`@{username}` hikoyasi ({index + 1}/{len(stories)})\n\n"

                            if mentions:
                                caption_text += f"Belgilashlar: {mentions}\n\n"
                            caption_text += f"{story_time}"

                            if story.video_url:
                                await bot.send_video(tg_id, FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")
                            else:
                                await bot.send_photo(tg_id, FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")

                            await bot.send_message(tg_id, f"✅ Yangi hikoya")

                            os.remove(file_name)

                            await update_last_story_time(tg_id=tg_id, username=username, new_time=time)

                    except Exception as e:
                        await bot.send_message(chat_id, f"Bo'lim: Auto Fetch Stories\nUser: {tg_id}\nXatolik: {e}")

        except Exception as e:
            await bot.send_message(chat_id, f"Bo'lim: Auto Fetch Stories\nUser: {tg_id}\nXatolik: {e}")
