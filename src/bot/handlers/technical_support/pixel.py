from telegram import Update
from telegram.constants import ChatType
from telegram.ext import MessageHandler, filters, ConversationHandler, ContextTypes, CommandHandler

from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.entrypoint import entrypoint_start_handler

from bot.handlers.technical_support.commands import RDP, CREATE_PIXEL_COMMAND, SHARE_PIXEL_COMMAND
from bot.handlers.utils.keyboards import pixel_request_keyboard, empty_reply_keyboard
from config.config import TECHNICAL_COMMAND_THREAD_CHAT_ID, TECHNICAL_COMMAND_CHAT_ID

CHOOSE_ACTION = 1
ENTER_PIXEL = 2


async def pixel_request_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Выберите необходимое действие в меню <b>пикселя</b>:",
            reply_markup=pixel_request_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def create_pixel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {CREATE_PIXEL_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на создание пикселя успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await pixel_request_start_handler(update, context)
    return CHOOSE_ACTION


async def share_pixel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Пожалуйста, напишите <b>ID пикселя</b> в сообщении ниже.",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return ENTER_PIXEL


async def enter_pixel_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    pixel_id = update.effective_message.text

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {SHARE_PIXEL_COMMAND.format('3838388', pixel_id)}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на пошарку пикселя успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await pixel_request_start_handler(update, context)
    return CHOOSE_ACTION


async def pixel_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.handlers.technical_support.rdp_request import rdp_request_start_handler

    await rdp_request_start_handler(update, context)
    return ConversationHandler.END


pixel_request_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Пиксель") & ~filters.COMMAND, pixel_request_start_handler)
    ],
    states={
        CHOOSE_ACTION: [
            MessageHandler(filters.Regex("Создать пиксель") & ~filters.COMMAND, create_pixel_handler),
            MessageHandler(filters.Regex("Пошарить пиксель") & ~filters.COMMAND, share_pixel_handler),
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, pixel_back_handler)
            # MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, technical_support_start_handler),
        ],
        ENTER_PIXEL: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, enter_pixel_handler),
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
