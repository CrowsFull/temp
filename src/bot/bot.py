import logging

import pytz
from telegram.ext import Application, PicklePersistence

from src.bot.handlers.entrypoint import entrypoint_handler
from src.bot.handlers.registration import registration_handler
from src.bot.handlers.video_instruction import video_instruction_handler
from src.bot.jobs.cheques import handle_message_queue
from src.config.bot import bot_config

logger = logging.getLogger(__name__)


class Bot:

    def __include_handlers(self) -> None:
        self.application.add_handler(entrypoint_handler)
        self.application.add_handler(registration_handler)
        self.application.add_handler(video_instruction_handler)

        logger.info("Handlers included.")

    def __include_jobs(self) -> None:
        moscow_tz = pytz.timezone('Europe/Moscow')

        self.job_queue.run_once(handle_message_queue, 5)

    def __create_persistence(self) -> None:
        self.persistence: PicklePersistence = PicklePersistence(filepath=self.persistence_file_path,
                                                                update_interval=self.persistence_update_interval)
        logger.info("Persistence created.")

    def __create_application(self) -> None:
        self.__create_persistence()

        self.application: Application = Application.builder().token(bot_config.TOKEN).connect_timeout(
            self.connect_timeout).build()

        self.job_queue = self.application.job_queue

        # self.application: Application = Application.builder().token(token).connect_timeout(30).persistence(
        # persistence=self.persistence).build()
        # self.__include_jobs()
        self.__include_handlers()

    def __init__(self) -> None:
        self.connect_timeout: int = 30
        self.persistence_update_interval = 3
        self.persistence_file_path = 'platform_bot_persistence'

        logger.info("Application creation started.")
        self.__create_application()
        logger.info("Application creation finished.")

    def start(self):
        logger.info("Application start up.")
        self.application.run_polling()
