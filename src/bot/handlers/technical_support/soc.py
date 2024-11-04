from telegram import Update
from telegram.constants import ChatType
from telegram.ext import MessageHandler, filters, ConversationHandler, ContextTypes, CommandHandler

from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.entrypoint import entrypoint_start_handler

from bot.handlers.technical_support.commands import RDP, CHANGE_SOC_COMMAND, BAN_SOC_COMMAND
from bot.handlers.utils.keyboards import empty_reply_keyboard, soc_request_keyboard
from config.config import TECHNICAL_COMMAND_THREAD_CHAT_ID, TECHNICAL_COMMAND_CHAT_ID

CHOOSE_ACTION = 1
ENTER_NEW_SOC = 2


async def soc_request_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Выберите необходимое действие в меню <b>SOC</b>:",
            reply_markup=soc_request_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def change_soc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {CHANGE_SOC_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на смену SOC успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await soc_request_start_handler(update, context)
    return CHOOSE_ACTION


async def ban_soc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Пожалуйста, напишите <b>название нового SOC</b> в сообщении ниже.",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return ENTER_NEW_SOC


async def enter_soc_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    new_soc = update.effective_message.text

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {BAN_SOC_COMMAND.format('3838388', new_soc)}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на бан SOC успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await soc_request_start_handler(update, context)
    return CHOOSE_ACTION


async def soc_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.handlers.technical_support.rdp_request import rdp_request_start_handler

    await rdp_request_start_handler(update, context)
    return ConversationHandler.END


soc_request_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("SOC") & ~filters.COMMAND, soc_request_start_handler)
    ],
    states={
        CHOOSE_ACTION: [
            MessageHandler(filters.Regex("Поменять SOC") & ~filters.COMMAND, change_soc_handler),
            MessageHandler(filters.Regex("Бан SOC") & ~filters.COMMAND, ban_soc_handler),
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, soc_back_handler)
            # MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, technical_support_start_handler),
        ],
        ENTER_NEW_SOC: [
            MessageHandler(filters.TEXT & ~filters.COMMAND, enter_soc_handler),
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
