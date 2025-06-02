import os
from datetime import datetime, timedelta

import requests
from aiogram import F
from aiogram.types import CallbackQuery
from aiogram.types import FSInputFile

from src.config import CHAT_ID
from src.keyboards.inline_keyboard import share_to_friends
from src.loader import dp
from src.orm.auto_fetch_stories import add_or_replace_autofetch_account, remove_follow
from src.utils.login_insta import cl


@dp.callback_query(F.data.startswith("view_current_stories"))
async def send_stories(callback: CallbackQuery):
    username = callback.data.split(":")[1]

    try:
        user_id = cl.user_id_from_username(username)
        stories = cl.user_stories(user_id)

        if not stories:
            await callback.message.answer(f"`@{username}` profilida hozircha hech qanday hikoyalar mavjud emas.",
                                          parse_mode="Markdown")
        else:
            await callback.message.answer(f"Yuklanmoqda {len(stories)} hikoyalar `@{username}`",
                                          parse_mode="Markdown")

        save_path = "media/stories_media/"
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

                    mentions = ' '.join([f"@{mention.user.username}" for mention in story.mentions])\
                        if story.mentions else ''

                    uzb_time = datetime.utcfromtimestamp(story.taken_at.timestamp()) + timedelta(hours=5)
                    story_time = uzb_time.strftime("%d.%m.%Y, %H:%M:%S UZB")

                    caption_text = (
                        f"`@{username}` hikoyasi ({index + 1}/{len(stories)})\n\n"
                    )

                    if mentions:
                        caption_text += f"Belgilashlar: `{mentions}`\n\n"

                    caption_text += f"{story_time}"

                    if story.video_url:
                        await callback.message.answer_video(FSInputFile(file_name), caption=caption_text,
                                                            parse_mode="Markdown")
                    else:
                        await callback.message.answer_photo(FSInputFile(file_name), caption=caption_text,
                                                            parse_mode="Markdown")

                    os.remove(file_name)
                else:
                    await callback.message.answer("Yuklab olishda xatolik yuz berdi.")

            except Exception as e:
                await callback.message.answer(f"❌ {index + 1}-hikoyani yuklashda xatolik")
                await callback.bot.send_message(CHAT_ID, f"❌ {index + 1}-hikoyani yuklashda xatolik: {e}")

        await callback.message.answer(f"Bot yoqdimi? Iltimos, bu haqda do'stlaringizga ham ayting.",

                                      reply_markup=share_to_friends())

    except Exception as e:
        await callback.message.answer(f"❌ Xatolik yuz berdi")
        await callback.bot.send_message(CHAT_ID, f"❌ Xatolik yuz berdi: {e}")


@dp.callback_query(F.data.startswith("follow_to_account"))
async def follow_to_accounts(callback: CallbackQuery):
    username = callback.data.split(":")[1]
    user_id = callback.from_user.id

    success = await add_or_replace_autofetch_account(tg_id=user_id, username=username)
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

    await remove_follow(tg_id=user_id, username=username)
    await callback.message.answer(f"`@{username}` muvaffaqiyatli o'chirildi",
                                  parse_mode="Markdown")
