import logging

from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CommandHandler, ContextTypes

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.bot.handlers.consts.messages import WELCOME_MESSAGE
from src.bot.handlers.utils.keyboards import entrypoint_keyboard

logger = logging.getLogger(__name__)


async def entrypoint_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text=WELCOME_MESSAGE.format(chat.full_name),
            reply_markup=entrypoint_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return ConversationHandler.END


entrypoint_handler = ConversationHandler(
    entry_points=[
        CommandHandler("start", entrypoint_start_handler),
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
