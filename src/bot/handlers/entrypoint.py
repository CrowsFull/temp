import logging
from http import HTTPStatus

import aiohttp
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes

from bot.handlers.cheques.activate import cheque_handler
from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.consts.messages import WELCOME_MESSAGE
from bot.handlers.utils.keyboards import entrypoint_keyboard
from config.api import api_config

logger = logging.getLogger(__name__)


async def entrypoint_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    msg_split = update.effective_message.text.split(" ")

    if len(msg_split) > 1:
        async with (aiohttp.ClientSession() as session):
            url = f"{api_config.api_url}/export/users/bytoken"

            token = msg_split[-1]

            params = {
                "token": token
            }

            async with session.get(url, headers=api_config.api_headers, params=params) as response:
                if response.status == HTTPStatus.OK:
                    user: dict = await response.json()
                else:
                    pass

            user_id = user["id"]

            url = f"{api_config.api_url}/export/users/telegram/{user_id}"

            data = {
                "telegramUid": chat.id,
                "firstName": chat.first_name,
                "lastName": chat.last_name,
                "username": chat.username
            }

            async with session.post(url, headers=api_config.api_headers, json=data) as response:

                if response.status == HTTPStatus.CREATED \
                        or response.status == HTTPStatus.OK:
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text="Привязка профиля прошла успешно✅",
                        # reply_markup=entrypoint_keyboard,
                        parse_mode=BASE_PARSE_MODE
                    )

                else:
                    pass
    else:
        # if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=WELCOME_MESSAGE.format(chat.full_name),
            reply_markup=entrypoint_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return ConversationHandler.END


async def info_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    await context.bot.send_message(
        chat_id=chat.id,
        text="Информация о данном чате:\n\n"
             f"<b>Название чата</b>: {chat.full_name}\n"
             f"<b>ID</b>: {chat.id}\n"
             f"<b>Тип чата</b>: {chat.type}\n",
        parse_mode=BASE_PARSE_MODE
    )

    return ConversationHandler.END


entrypoint_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", entrypoint_start_handler),
        CommandHandler("info", info_handler),
        cheque_handler
    ],
    states={
        # START_STATE: [CallbackQueryHandler(auth_handler, f"^{MAIN_MENU_CALLBACKS["Авторизоваться"]}$")],
        # AUTH_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_enter_handler)]
    },
    fallbacks=[
        CommandHandler("start", entrypoint_start_handler)]
    # persistent=True,
    # name="conversation_handler_auth"
)
