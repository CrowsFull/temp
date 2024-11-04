from telegram import Update
from telegram.constants import ChatType
from telegram.ext import MessageHandler, filters, ConversationHandler, ContextTypes, CommandHandler

from bot.handlers.consts.consts import BASE_PARSE_MODE
from bot.handlers.entrypoint import entrypoint_start_handler
from bot.handlers.technical_support.account_problem import account_problem_request_handler
from bot.handlers.technical_support.checkpoint import checkpoint_request_handler
from bot.handlers.technical_support.funpage import funpage_request_handler
from bot.handlers.technical_support.pixel import pixel_request_handler
from bot.handlers.technical_support.soc import soc_request_handler
from bot.handlers.utils.keyboards import akk_request_keyboard

CHOOSE_ACTION = 1


async def akk_request_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="AKK",
            reply_markup=akk_request_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def akk_request_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from bot.handlers.technical_support.base import technical_support_start_handler

    await technical_support_start_handler(update, context)
    return ConversationHandler.END


akk_request_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Запросы по AKK") & ~filters.COMMAND, akk_request_start_handler)
    ],
    states={
        CHOOSE_ACTION: [
            pixel_request_handler,
            checkpoint_request_handler,
            soc_request_handler,
            funpage_request_handler,
            account_problem_request_handler,
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, akk_request_back_handler)
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
