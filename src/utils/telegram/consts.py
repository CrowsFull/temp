from pyrogram import Client

from config.bot import bot_config

BASE_GROUP_LIST = ["platformtesttest_bot",
                   ]
BASE_CHAT_TITLE = "TrustChat"

app = Client("session",
             api_id=bot_config.ID,
             api_hash=bot_config.HASH)
