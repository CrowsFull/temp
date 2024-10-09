from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup

from src.bot.handlers.utils.buttons import *

entrypoint_keyboard = InlineKeyboardMarkup([
    [registration_button]
])

activate_keyboard = InlineKeyboardMarkup([
    [activate_button]
])

first_menu_keyboard = InlineKeyboardMarkup([
    [video_instruction_button]
])

first_menu_reply_keyboard = ReplyKeyboardMarkup([
    [select_account_button],
    [top_up_balance_button],
    [active_accounts_button],
    [extend_team_button, technical_support_button]
])
