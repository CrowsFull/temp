from telegram import InlineKeyboardMarkup, ReplyKeyboardMarkup, ReplyKeyboardRemove

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
], resize_keyboard=True)

technical_support_reply_keyboard = ReplyKeyboardMarkup([
    [reference_information_button],
    [rdp_request_button],
    [akk_request_button],
    [back_button]
], resize_keyboard=True)

rdp_request_keyboard = ReplyKeyboardMarkup([
    [pixel_button, checkpoint_button],
    [soc_button, fun_page_button],
    [account_problem_button],
    [request_back_button, support_button]
], resize_keyboard=True)

akk_request_keyboard = ReplyKeyboardMarkup([
    [pixel_button, checkpoint_button],
    [soc_button, fun_page_button],
    [account_problem_button],
    [request_back_button, support_button]
], resize_keyboard=True)

pixel_request_keyboard = ReplyKeyboardMarkup([
    [create_pixel_button],
    [share_pixel_button],
    [back_button]
], resize_keyboard=True)

empty_reply_keyboard = ReplyKeyboardRemove()

checkpoint_request_keyboard = ReplyKeyboardMarkup([
    [make_checkpoint_button],
    [back_button]
], resize_keyboard=True)

soc_request_keyboard = ReplyKeyboardMarkup([
    [change_soc_button],
    [ban_soc_button],
    [back_button]
], resize_keyboard=True)

funpage_request_keyboard = ReplyKeyboardMarkup([
    [create_funpage_button],
    [error_funpage_button],
    [back_button]
], resize_keyboard=True)

account_problem_request_button = ReplyKeyboardMarkup([
    [ban_account_button],
    [ban_account_zrd_button],
    [no_limit_button],
    [no_spend_button, policy_error_button],
    [back_button]
], resize_keyboard=True)
