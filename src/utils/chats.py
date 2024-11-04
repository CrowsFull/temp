import logging
from telegram.client import Telegram
from typing import List, Dict
import asyncio

# Настройка логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Инициализация клиента TDLib
tg = Telegram(
    api_id='22978305',  # Замените на ваш api_id
    api_hash='9439394aaec4b6477f8a7b0cce18b045',  # Замените на ваш api_hash
    database_encryption_key="djsfjknfcksndfjk"
)


# Асинхронная функция для создания группового чата
async def create_group_chat(chat_name: str, users: List[int], bots: List[Dict[str, str]]):
    tg.login()
    logger.info(f"Creating new group chat with users: {', '.join(map(str, users))}")

    # Кэшируем информацию о ботах, чтобы их можно было добавлять в чат
    for bot in bots:
        await tg.get_chat(bot['botId'])

    # Создаем групповой чат
    chat = await tg.create_new_basic_group_chat(user_ids=users, title=chat_name)
    created_chat_id = chat['id']

    logger.info(f"Created new group chat: {chat_name}, id: {created_chat_id}")

    # Приглашаем ботов в чат
    for bot in bots:
        await tg.send_bot_start_message(bot_user_id=bot['botId'], chat_id=created_chat_id, parameter='invited')

    logger.info(f"Invited bots to chat (id={created_chat_id}): {[bot['botUsername'] for bot in bots]}")
    tg.stop()


# Запуск
# Выполните вход для TDLib
asyncio.run(create_group_chat("New Group", [12345678], [{'botId': 987654321, 'botUsername': 'my_bot'}]))

# Не забывайте останавливать клиента после завершения работы


"""
import logging
from td.client import TdClient
from rx import last_value_from
from rx.operators import filter, take
from typing import List, Dict

# Конфигурация логгера
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


# Функция для создания группового чата
async def create_group_chat(chat_name: str, users: List[int], bots: List[Dict[str, str]]) -> Dict:
    logger.info(f"Creating new group chat with users: {', '.join(map(str, users))}")

    client = TdClient()

    # Получаем информацию о каждом пользователе
    for user_id in users:
        await client.execute({'@type': 'getUser', 'user_id': user_id})

    # Кэшируем информацию о каждом боте для TDLib
    for bot in bots:
        await client.execute({'@type': 'searchPublicChat', 'username': bot['botUsername']})

    # Создаем групповой чат
    chat = await client.execute({
        '@type': 'createNewBasicGroupChat',
        'title': chat_name,
        'user_ids': users
    })
    created_chat_id = chat['id']

    # Получаем информацию о чате
    chat_info = await last_value_from(client.get_chat_info(created_chat_id).pipe(
        filter(lambda i: i['id'] == created_chat_id),
        take(1)
    ))

    # Получаем полную информацию о группе
    group_info = await last_value_from(client.get_group_full_info(chat_info['basic_group_id']).pipe(
        filter(lambda i: i['id'] == chat_info['basic_group_id']),
        take(1)
    ))

    logger.info(f"Created new group chat: {chat_name}, id: {created_chat_id}, groupId: {group_info['id']}")

    # Ждем, пока боты добавятся в группу
    bots_added = last_value_from(client.get_updates().pipe(
        filter(lambda t: t['@type'] == 'updateBasicGroupFullInfo' and
                         t['basic_group_id'] == group_info['id'] and
                         len(t['basic_group_full_info']['members']) >= len(users) + len(bots)),
        take(1)
    ))

    # Приглашаем ботов в чат
    for bot in bots:
        await client.execute({
            '@type': 'sendBotStartMessage',
            'bot_user_id': bot['botId'],
            'chat_id': created_chat_id,
            'parameter': 'invited'
        })

    logger.info(f"Invited bots to chat (id={created_chat_id}): {[bot['botUsername'] for bot in bots]}")

    # Ожидаем подтверждения добавления ботов
    await bots_added
    logger.info(f"Bots were added to chat (id={created_chat_id})")

    return {
        'chat_id': created_chat_id,
        'group_id': group_info['id']
    }
"""
