from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class BotConfig(BaseSettings):
    """ Bot configuration class"""
    TOKEN: str
    DEBUG: bool

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"


bot_config = BotConfig()
