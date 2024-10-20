from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class APIConfig(BaseSettings):
    """ Bot configuration class"""
    API_HOST: str
    API_PORT: str
    API_TOKEN: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"


api_config = APIConfig()
