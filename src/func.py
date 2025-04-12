import os
from datetime import datetime, timedelta

import requests
from aiogram import Bot
from aiogram.types import FSInputFile
from sqlalchemy.ext.asyncio import AsyncSession

from src.login_instagram import cl
from src.orm import get_user_accounts


async def send_stories_to_user(bot: Bot, session: AsyncSession, tg_id: int):
    accounts = await get_user_accounts(session, tg_id)

    for username in accounts:
        try:
            user_id = cl.user_id_from_username(username)
            stories = cl.user_stories(user_id)

            if stories:
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
                            caption_text = f"`@{username}` hikoyasi ({index + 1}/{len(stories)})\n\n"

                            if mentions:
                                caption_text += f"Metka: `{mentions}`\n\n"
                            caption_text += f"{story_time}"

                            if story.video_url:
                                await bot.send_video(tg_id, FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")
                            else:
                                await bot.send_photo(tg_id, FSInputFile(file_name), caption=caption_text, parse_mode="Markdown")

                            os.remove(file_name)
                        else:
                            await bot.send_message(tg_id, f"`@{username}` hikoyasini yuklab bo‘lmadi.", parse_mode="Markdown")

                    except Exception as e:
                        await bot.send_message(tg_id, f"❌ {index + 1}-hikoyani yuklashda xatolik: {e}", parse_mode="Markdown")

        except Exception as e:
            await bot.send_message(tg_id, f"❌ `@{username}` uchun xatolik: {e}", parse_mode="Markdown")
