import logging

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes, CallbackQueryHandler, filters, \
    MessageHandler

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.bot.handlers.consts.messages import ACTIVATE_MESSAGE, REGISTRATION_MESSAGE, FIRST_MENU_MESSAGE, \
    FIRST_MAIN_MENU_MESSAGE
from src.bot.handlers.entrypoint import entrypoint_start_handler
from src.bot.handlers.technical_support.base import technical_support_start_handler, technical_support_handler
from src.bot.handlers.utils.keyboards import activate_keyboard, first_menu_keyboard, first_menu_reply_keyboard

logger = logging.getLogger(__name__)

ACTIVATE_BOT = 1
ENTER_INFORMATION = 2
CHOOSE_ACTION = 3
MAIN_MENU = 4


async def registration_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # todo: chat create logic

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=REGISTRATION_MESSAGE,
            reply_markup=activate_keyboard,
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
