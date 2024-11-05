import asyncio

from utils.telegram.consts import app, BASE_GROUP_LIST


def create_client_connection(func):
    async def wrapper(*args, **kwargs):
        await app.start()
        try:
            result = await func(app, *args, **kwargs)
        finally:
            await app.stop()
        return result

    return wrapper


@create_client_connection
async def create_group_chat(app, chat_title, usernames):
    """
    Создает группу и добавляет пользователей.

    :param chat_title: Название группы
    :param usernames: Список username пользователей для добавления
    """
    chat = await app.create_group(title=chat_title, users=usernames)
    return chat


@create_client_connection
async def create_invite_link(app, chat):
    invite_link = await app.create_chat_invite_link(chat_id=chat.id, expire_date=None)
    return invite_link.invite_link
