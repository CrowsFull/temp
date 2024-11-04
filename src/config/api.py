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

    @property
    def api_url(self):
        return f"http://{self.API_HOST}:{self.API_PORT}/api"

    @property
    def api_headers(self):
        return {
            "X-Api-Key": self.API_TOKEN,
            "accept": "application/json"
        }


api_config = APIConfig()
