import logging
import uuid
from http import HTTPStatus

import aiohttp
from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, CallbackQueryHandler, filters, \
    MessageHandler

from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.consts.messages import ACTIVATE_MESSAGE, REGISTRATION_MESSAGE, FIRST_MENU_MESSAGE, \
    FIRST_MAIN_MENU_MESSAGE
from bot.handlers.entrypoint import entrypoint_start_handler
from bot.handlers.technical_support.base import technical_support_handler
from bot.handlers.utils.keyboards import activate_keyboard, first_menu_keyboard, first_menu_reply_keyboard
from config.api import api_config
from utils.telegram.chats import create_group_chat, create_invite_link
from utils.telegram.consts import BASE_CHAT_TITLE, BASE_GROUP_LIST

logger = logging.getLogger(__name__)

ACTIVATE_BOT = 1
ENTER_INFORMATION = 2
CHOOSE_ACTION = 3
MAIN_MENU = 4


async def registration_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        usernames = BASE_GROUP_LIST
        usernames.append(chat.username)

        new_chat = await create_group_chat(chat_title=BASE_CHAT_TITLE,
                                           usernames=usernames)

        invite_link: str = await create_invite_link(new_chat)

        data = {
            "chatId": new_chat.id,
            "inviteLink": invite_link
        }

        project_id = 1

        async with aiohttp.ClientSession() as session:
            url = f"{api_config.api_url}/export/projects/tgchat/{project_id}"

            async with session.put(url, headers=api_config.api_headers, json=data) as response:
                if response.status == HTTPStatus.OK:
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text=REGISTRATION_MESSAGE.format(invite_link),
                        reply_markup=activate_keyboard,
                        disable_web_page_preview=True,
                        parse_mode=BASE_PARSE_MODE
                    )

                    await context.bot.send_message(
                        chat_id=new_chat.id,
                        text="Приветик!",
                        disable_web_page_preview=True,
                        parse_mode=BASE_PARSE_MODE
                    )
                else:
                    await context.bot.send_message(
                        chat_id=chat.id,
                        text="Возникла ошибка при создании чата.",
                        parse_mode=BASE_PARSE_MODE
                    )

        return ACTIVATE_BOT


async def activate_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=ACTIVATE_MESSAGE,
            parse_mode=BASE_PARSE_MODE
        )

    return ENTER_INFORMATION


async def enter_information_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = update.effective_message.text

    if "," not in message:
        pass
        # todo: error

    name, email = message.split(",")

    # todo: save info

    await main_menu_handler(update, context)
    return CHOOSE_ACTION


async def main_menu_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=FIRST_MENU_MESSAGE,
            reply_markup=first_menu_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=FIRST_MAIN_MENU_MESSAGE,
            reply_markup=first_menu_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def choose_action_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    message = update.effective_message.text

    await context.bot.send_message(
        chat_id=chat.id,
        text="dnhjdhdhdj",
        reply_markup=first_menu_reply_keyboard,
        parse_mode=BASE_PARSE_MODE
    )

    match message:
        case "Баланс":
            pass
        case "Активные аккаунты":
            pass
        case "Расширить свою команду":
            pass
        case _:
            await main_menu_handler(update, context)
            return CHOOSE_ACTION


async def unknown_message_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    await context.bot.send_message(
        chat_id=chat.id,
        text="Неизвестная команда.",
        parse_mode=BASE_PARSE_MODE
    )

    await main_menu_handler(update, context)
    return CHOOSE_ACTION


registration_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=registration_start_handler,
                             pattern="^registration_action$"),
    ],
    states={
        ACTIVATE_BOT: [CallbackQueryHandler(activate_handler, "^activate_action$")],
        ENTER_INFORMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_information_handler)],
        CHOOSE_ACTION: [MessageHandler(filters.Regex("Подобрать аккаунт") & ~filters.COMMAND, choose_action_handler),
                        MessageHandler(filters.Regex("Баланс") & ~filters.COMMAND, choose_action_handler),
                        MessageHandler(filters.Regex("Активные аккаунты") & ~filters.COMMAND, choose_action_handler),
                        MessageHandler(filters.Regex("Расширить свою команду") & ~filters.COMMAND,
                                       choose_action_handler),
                        technical_support_handler,
                        MessageHandler(filters.TEXT & ~filters.COMMAND, unknown_message_handler)],
        # START_STATE: [CallbackQueryHandler(auth_handler, f"^{MAIN_MENU_CALLBACKS["Авторизоваться"]}$")],
        # AUTH_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_enter_handler)]
    },
    fallbacks=[
        CommandHandler("start", entrypoint_start_handler)]
    # persistent=True,
    # name="conversation_handler_auth"
)
