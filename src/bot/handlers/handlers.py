import os
import requests
from aiogram import Bot
from aiogram.types import Message
from aiogram.filters import Command
from aiogram.types import FSInputFile

from src.config.loader import dp
from src.config.config import settings
from src.database.orm.orm import add_user
from src.i18n.i18n_setup import _
from src.utils.login_insta import cl
from src.database.orm.auto_fetch_stories import get_autofetch_accounts
from src.bot.keyboards.inline_keyboard import delete_profile_button
from src.bot.keyboards.inline_keyboard import private_profile_button
from src.bot.keyboards.inline_keyboard import support_button, share_to_chat, select_language

chat_id = settings.CHAT_ID


async def startup_answer(bot: Bot):
    await bot.send_message(chat_id, _("Бот успешно запущен! ✅"))


async def shutdown_answer(bot: Bot):
    await bot.send_message(chat_id, _("Бот остановлен.! ❌"))


@dp.message(Command("start"))
async def start(message: Message, bot: Bot):
    user_added = await add_user(
        tg_id=message.from_user.id,
        fullname=message.from_user.full_name,
        username=message.from_user.username,
    )

    if user_added:
        await bot.send_message(chat_id, _("Зарегистрирован новый пользователь! ✅"))

    await message.answer(_("Привет, я Стори Шэдоув — твой персональный Instagram шпион.\n"
                            "Я помогу тебе анонимно следить за чужими историями и публикациями.\n"
                            "Отправь имя пользователя или ссылку на инстаграм того, кто тебя интересует."))


@dp.message(Command("get"))
async def get(message: Message):
    await message.answer(_("Отправь имя пользователя или ссылку на инстаграм того, кто тебя интересует."))


@dp.message(Command("chats"))
async def chat(message: Message):
    await message.answer(_("Добавляй бота @storyshadowbot в свой чат, если хочешь автоматически публиковать в нем истории и публикации.\n"
                           "Только владелец чата может выбрать, что в нем публиковать.\n\n"
                           "Список твоих чатов, в которых состоит бот: пуст"), reply_markup=share_to_chat())


@dp.message(Command("support"))
async def support(message: Message):
    await message.answer(_("Связаться с нами:"), reply_markup=support_button())


@dp.message(Command("help"))
async def help_bot(message: Message):
    await message.answer(_(f"Необходимые команды:\n\n"
                         f"/start — Перезапустить бота\n"
                         f"/get — Просмотреть истории\n"
                         f"/subscription — Просмотреть подписки\n"
                         f"/chats — Просмотреть чаты\n"
                         f"/support — Получить поддержку"))
    

@dp.message(Command("language"))
async def language(message: Message):
    await message.answer(_("Выберите язык:"), reply_markup=select_language())    


@dp.message(Command("subscription"))
async def follow_list(message: Message, bot: Bot, save_path="media/users_media/"):
    tg_id = message.from_user.id
    account = await get_autofetch_accounts(tg_id)

    wait_msg = await message.answer("⌛️")

    for username in account:
        try:
            user_info = cl.user_info_by_username(username, use_cache=False)
            is_private = user_info.is_private
            account_status = _("`@{username}` - Закрытый аккаунт.").format(username=username) if is_private else f"`@{username}`"
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
            await bot.send_message(chat_id, _("Раздел: Auto Fetch Stories\nUser: {tg_id}\nОшибка: {e}").format(tg_id=tg_id, e=e))

    await bot.delete_message(message.chat.id, wait_msg.message_id)