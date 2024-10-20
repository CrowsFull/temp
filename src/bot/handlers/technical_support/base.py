from telegram import Update
from telegram.constants import ChatType
from telegram.ext import ConversationHandler, CallbackQueryHandler, CommandHandler, ContextTypes, MessageHandler, \
    filters, BaseHandler

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.bot.handlers.entrypoint import entrypoint_start_handler

from src.bot.handlers.technical_support.akk_request import akk_request_handler
from src.bot.handlers.technical_support.rdp_request import rdp_request_handler
from src.bot.handlers.utils.keyboards import technical_support_reply_keyboard, empty_reply_keyboard

CHOOSE_ACTION = 1


async def technical_support_start_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Ниже представлены самые частые запросы, если  Вашего вопроса "
                 "нет среди них просто напишите в чат!\n\n"
                 "Вам ответит первый освободившийся оператор.",
            reply_markup=technical_support_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    return CHOOSE_ACTION


async def reference_information_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    chat = update.effective_chat

    if chat.type == ChatType.PRIVATE:
        await context.bot.send_message(
            chat_id=chat.id,
            text="Здесь будет справочная информация.",
            reply_markup=empty_reply_keyboard,
            parse_mode=BASE_PARSE_MODE
        )

    await technical_support_start_handler(update, context)
    return CHOOSE_ACTION


async def reference_information_back_handler(update: Update, context: ContextTypes.DEFAULT_TYPE):
    from src.bot.handlers.registration import main_menu_handler

    await main_menu_handler(update, context)
    return ConversationHandler.END


technical_support_handler = ConversationHandler(
    entry_points=[
        MessageHandler(filters.Regex("Тех. поддержка") & ~filters.COMMAND,
                       technical_support_start_handler),
    ],
    states={
        CHOOSE_ACTION: [
            MessageHandler(filters.Regex("Справочная информация") & ~filters.COMMAND, reference_information_handler),
            rdp_request_handler,
            akk_request_handler,
            MessageHandler(filters.Regex("Назад") & ~filters.COMMAND, reference_information_back_handler),
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
