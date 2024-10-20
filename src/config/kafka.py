from dotenv import load_dotenv
from pydantic_settings import BaseSettings

load_dotenv()


class KafkaConfig(BaseSettings):
    """ Bot configuration class"""
    KAFKA_BROKER_URL: str
    KAFKA_GROUP_ID: str

    class Config:
        env_file = ".env"
        env_file_encoding = 'utf-8'
        extra = "ignore"


kafka_config = KafkaConfig()
