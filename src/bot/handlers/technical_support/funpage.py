from telegram import Update
from telegram.constants import ChatType
from telegram.ext import MessageHandler, filters, ConversationHandler, ContextTypes, CommandHandler

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.bot.handlers.entrypoint import entrypoint_start_handler

from src.bot.handlers.technical_support.commands import RDP, ERROR_FUNPAGE_COMMAND, CREATE_FUNPAGE_COMMAND
from src.bot.handlers.utils.keyboards import empty_reply_keyboard, funpage_request_keyboard
from src.config.config import TECHNICAL_COMMAND_THREAD_CHAT_ID, TECHNICAL_COMMAND_CHAT_ID

CHOOSE_ACTION = 1


async def funpage_request_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Выберите необходимое действие в меню <b>FunPage</b>:",
            reply_markup=funpage_request_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def create_funpage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {CREATE_FUNPAGE_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на создание FunPage успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await funpage_request_start_handler(update, context)
    return CHOOSE_ACTION


async def error_funpage_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {ERROR_FUNPAGE_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы FunPage успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await funpage_request_start_handler(update, context)
    return CHOOSE_ACTION


async def funpage_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.handlers.technical_support.rdp_request import rdp_request_start_handler

    await rdp_request_start_handler(update, context)
    return ConversationHandler.END


funpage_request_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("FunPage") & ~filters.COMMAND, funpage_request_start_handler)
    ],
    states={
        CHOOSE_ACTION: [
            MessageHandler(filters.Regex("Создать FunPage") & ~filters.COMMAND, create_funpage_handler),
            MessageHandler(filters.Regex("Ошибка FunPage") & ~filters.COMMAND, error_funpage_handler),
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, funpage_back_handler)
            # MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, technical_support_start_handler),
        ]
        # ACTIVATE_BOT: [CallbackQueryHandler(activate_handler, "^activate_action$")],
        # ENTER_INFORMATION: [MessageHandler(filters.TEXT & ~filters.COMMAND, enter_information_handler)]
        # START_STATE: [CallbackQueryHandler(auth_handler, f"^{MAIN_MENU_CALLBACKS["Авторизоваться"]}$")],
        # AUTH_STATE: [MessageHandler(filters.TEXT & ~filters.COMMAND, auth_enter_handler)]
    },
    fallbacks=[
        CommandHandler("start", entrypoint_start_handler)]
    # persistent=True,
    # name="conversation_handler_auth"
)
