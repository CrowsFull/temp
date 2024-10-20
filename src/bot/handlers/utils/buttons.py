from telegram import InlineKeyboardButton, KeyboardButton

registration_button = InlineKeyboardButton(text="Ваш персональный чат",
                                           callback_data="registration_action")

activate_button = InlineKeyboardButton(text="Активировать бота",
                                       callback_data="activate_action")

video_instruction_button = InlineKeyboardButton(text="Видеоинструкции",
                                                callback_data="video_instruction_action")

# -------------
select_account_button = KeyboardButton(text="Подобрать аккаунт")
top_up_balance_button = KeyboardButton(text="Баланс")
active_accounts_button = KeyboardButton(text="Активные аккаунты")
extend_team_button = KeyboardButton(text="Расширить свою команду")
technical_support_button = KeyboardButton(text="Тех. поддержка")

account_settings_button = InlineKeyboardButton(text="⚙️",
                                               callback_data="account_settings_action")

# ----------------
reference_information_button = KeyboardButton(text="Справочная информация")
rdp_request_button = KeyboardButton(text="Запросы по RDP")
akk_request_button = KeyboardButton(text="Запросы по AKK")

# -------

pixel_button = KeyboardButton(text="Пиксель")
checkpoint_button = KeyboardButton(text="CheckPoint")
soc_button = KeyboardButton(text="SOC")
fun_page_button = KeyboardButton(text="FunPage")
account_problem_button = KeyboardButton(text="Проблемы с аккаунтом")
request_back_button = KeyboardButton(text="Назад")
support_button = KeyboardButton(text="Поддержка")

# ------------
create_pixel_button = KeyboardButton(text="Создать пиксель")
share_pixel_button = KeyboardButton(text="Пошарить пиксель")

# -----
make_checkpoint_button = KeyboardButton(text="Пройти CheckPoint")

# ------
change_soc_button = KeyboardButton(text="Поменять SOC")
ban_soc_button = KeyboardButton(text="Бан SOC")

# ------
create_funpage_button = KeyboardButton(text="Создать FunPage")
error_funpage_button = KeyboardButton(text="Ошибка FunPage")

# ------
ban_account_button = KeyboardButton(text="Бан аккаунта")
ban_account_zrd_button = KeyboardButton(text="Бан аккаунта - ЗРД")
no_limit_button = KeyboardButton(text="Слетел лимит")
no_spend_button = KeyboardButton(text="Нет спенда")
policy_error_button = KeyboardButton(text="Полиси ошибка")

back_button = KeyboardButton(text="Назад")
