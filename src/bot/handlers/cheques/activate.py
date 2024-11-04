import logging
from http import HTTPStatus

import aiohttp
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, ContextTypes

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.config.api import api_config


async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.handlers.entrypoint import entrypoint_start_handler

    chat = update.effective_chat
    chat_type = chat.type

    project_name = " ".join(update.effective_message.text.split(" ")[1:])

    message = None

    if chat_type == ChatType.GROUP or chat_type == ChatType.SUPERGROUP:
        try:
            async with aiohttp.ClientSession() as session:
                url = f"{api_config.api_url}/export/projects/byname"

                params = {
                    "name": project_name
                }

                async with session.get(url, headers=api_config.api_headers, params=params) as response:
                    if response.status == HTTPStatus.OK:
                        project: dict = await response.json()
                    else:
                        pass

                project_id = project['id']

                url = f"{api_config.api_url}/export/projects/tgchat/{project_id}"

                data = {
                    "chatId": chat.id,
                    "inviteLink": "tg"
                }

                async with session.put(url, headers=api_config.api_headers, data=data) as response:

                    if response.status == HTTPStatus.OK:
                        result: dict = await response.json()
                    else:
                        logging.error(f"{response.status}: ERROR")
                        return False

                message = ('Вы успешно активировали функцию <b>"Отправка чеков в чат"</b>🥳\n\n'
                           'Полученная информация:\n'
                           f'1. <b>Telegram Id:</b> {chat.id}\n'
                           f'2. <b>Название проекта:</b> {project_name}')
        except Exception as e:
            logging.error(e)
            return False
    elif chat_type == ChatType.PRIVATE or chat_type == ChatType.CHANNEL:
        message = 'К сожалению, данная команда работает только в чате типа <b>"Группа"</b>😢'

    await context.bot.send_message(
        chat_id=chat.id,
        text=message,
        parse_mode=BASE_PARSE_MODE
    )

    # chat_id = int(projects[project_name]["partner_chat_id"])

    await entrypoint_start_handler(update, context)
    return ConversationHandler.END


async def activate_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.handlers.entrypoint import entrypoint_start_handler

    await entrypoint_start_handler(update, context)
    return ConversationHandler.END


cheque_handler = ConversationHandler(
    entry_points=[
        CommandHandler("partner_chat", activate_handler)
    ],
    states={
        # ACTIVATE_BOT: [CallbackQueryHandler(activate_handler, "^activate_action$")],
        # ENTER_INFORMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_information_handler)]
        # START_STATE: [CallbackQueryHandler(auth_handler, f"^{MAIN_MENU_CALLBACKS["Авторизоваться"]}$")],
        # AUTH_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_enter_handler)]
    },
    fallbacks=[
        CommandHandler("start", activate_back_handler)]
    # persistent=True,
    # name="conversation_handler_auth"
)
