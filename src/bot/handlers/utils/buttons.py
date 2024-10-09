from telegram import InlineKeyboardButton, KeyboardButton

registration_button = InlineKeyboardButton(text="Ваш персональный чат",
                                           callback_data="registration_action")

activate_button = InlineKeyboardButton(text="Активировать бота",
                                       callback_data="activate_action")

video_instruction_button = InlineKeyboardButton(text="Видеоинструкции",
                                                callback_data="video_instruction_action")

# -------------
select_account_button = KeyboardButton(text="Подобрать аккаунт")
top_up_balance_button = KeyboardButton(text="Пополнить баланс")
active_accounts_button = KeyboardButton(text="Активные аккаунты")
extend_team_button = KeyboardButton(text="Расширить свою команду")
technical_support_button = KeyboardButton(text="Тех. поддержка")
