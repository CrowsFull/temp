from telegram import Update
from telegram.constants import ChatType
from telegram.ext import MessageHandler, filters, ConversationHandler, ContextTypes, CommandHandler

from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.entrypoint import entrypoint_start_handler

from bot.handlers.technical_support.commands import RDP, BAN_ACCOUNT_ZRD_COMMAND, BAN_ACCOUNT_COMMAND, \
    LIMIT_ACCOUNT_COMMAND, SPEND_ACCOUNT_COMMAND, POLICY_ACCOUNT_COMMAND
from bot.handlers.utils.keyboards import empty_reply_keyboard, \
    account_problem_request_button
from config.config import TECHNICAL_COMMAND_THREAD_CHAT_ID, TECHNICAL_COMMAND_CHAT_ID

CHOOSE_ACTION = 1


async def account_problem_request_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Выберите необходимое действие в меню <b>проблем аккаунта</b>:",
            reply_markup=account_problem_request_button,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def ban_account_problem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {BAN_ACCOUNT_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы бана аккаунта успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await account_problem_request_start_handler(update, context)
    return CHOOSE_ACTION


async def ban_account_problem_zrd_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {BAN_ACCOUNT_ZRD_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы бана аккаунта ЗРД успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await account_problem_request_start_handler(update, context)
    return CHOOSE_ACTION


async def limit_account_problem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {LIMIT_ACCOUNT_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы лимита отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await account_problem_request_start_handler(update, context)
    return CHOOSE_ACTION


async def spend_account_problem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {SPEND_ACCOUNT_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы бана спенда отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await account_problem_request_start_handler(update, context)
    return CHOOSE_ACTION


async def policy_account_problem_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=TECHNICAL_COMMAND_CHAT_ID,
            message_thread_id=TECHNICAL_COMMAND_THREAD_CHAT_ID,
            text=f"{RDP} {POLICY_ACCOUNT_COMMAND.format('3838388')}",
            parse_mode=BASE_PARSE_MODE
        )

        await context.bot.send_message(
            chat_id=chat.id,
            text=f"Заявка на решение проблемы полиси успешно отправлена!",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await account_problem_request_start_handler(update, context)
    return CHOOSE_ACTION


async def account_problem_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.handlers.technical_support.rdp_request import rdp_request_start_handler

    await rdp_request_start_handler(update, context)
    return ConversationHandler.END


account_problem_request_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Проблемы с аккаунтом") & ~filters.COMMAND, account_problem_request_start_handler)
    ],
    states={
        CHOOSE_ACTION: [
            MessageHandler(filters.Regex("^Бан аккаунта$") & ~filters.COMMAND, ban_account_problem_handler),
            MessageHandler(filters.Regex("Бан аккаунта - ЗРД") & ~filters.COMMAND, ban_account_problem_zrd_handler),
            MessageHandler(filters.Regex("Слетел лимит") & ~filters.COMMAND, limit_account_problem_handler),
            MessageHandler(filters.Regex("Нет спенда") & ~filters.COMMAND, spend_account_problem_handler),
            MessageHandler(filters.Regex("Полиси ошибка") & ~filters.COMMAND, policy_account_problem_handler),
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, account_problem_back_handler),
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
