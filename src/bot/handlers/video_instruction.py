from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, ContextTypes

from bot.handlers.consts.consts import BASE_PARSE_MODE
from src.bot.handlers.entrypoint import entrypoint_start_handler


async def video_instruction_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    # todo: chat create logic

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Здесь информация о видеоинструкции.",
            parse_mode=BASE_PARSE_MODE
        )

    return ConversationHandler.END


video_instruction_handler = ConversationHandler(
    entry_points=[
        CallbackQueryHandler(callback=video_instruction_handler,
                             pattern="^video_instruction_action$"),
    ],
    states={
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
