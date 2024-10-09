import logging

from src.bot.bot import Bot
from src.config.bot import bot_config

logging.basicConfig(level=bot_config.DEBUG)


if __name__ == "__main__":
    bot: Bot = Bot()
    bot.start()
