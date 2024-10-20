import json
import logging
from typing import List

from confluent_kafka import Consumer, KafkaError
from telegram import Bot

from src.bot.handlers.consts.consts import BASE_PARSE_MODE
from src.config.config import TECHNICAL_COMMAND_CHAT_ID
from src.config.kafka import kafka_config
from src.kafka.enums import KafkaTopic


class KafkaConsumerManager:

    def __init__(self, broker_url: str, topics: List[str]):
        self.consumer_conf: dict = {
            'bootstrap.servers': broker_url,
            'group.id': 'telegram_bot_group',
            'auto.offset.reset': 'earliest'
        }

        self.topics: List[str] = topics

        self.consumer: Consumer = Consumer(self.consumer_conf)
        logging.info("Kafka consumer initialized.")

        self.consumer.subscribe(topics)
        logging.info(f"Kafka consumer subscribed on topics {','.join(topics)}.")

        self.timeout = 1.0

    async def handle_kafka_messages(self, bot: Bot):
        while True:
            msg = self.consumer.poll(self.timeout)

            if msg is None:
                continue

            msg_error = msg.error()

            if msg_error:
                if msg_error.code() == KafkaError._PARTITION_EOF:
                    continue
                else:
                    logging.error(f"Ошибка Kafka: {msg_error}")
                    break

            try:
                message_topic = msg.topic()

                if message_topic == KafkaTopic.PARTNER_CHEQUES:
                    data = json.loads(msg.value().decode('utf-8'))
                    # TODO: add tpe - type of event?
                    partner_chat_id = data.get("partner_chat_id")
                    client_chat_id = data.get("client_chat_id")
                    project = data.get("project")
                    status = data.get("status")
                    price = data.get("price")
                    link = data.get("link")

                    if status == "finished":
                        await bot.send_message(
                            chat_id=partner_chat_id,
                            text="<b>Информация по чеку</b>\n\n"
                                 f"<b>Проект</b>: {project}\n"
                                 f"<b>Сумма</b>: {price}$\n"
                                 f"<b>Ссылка</b>: {link}",
                            parse_mode=BASE_PARSE_MODE,
                        )

                        partner_chat = await bot.get_chat(partner_chat_id)

                        await bot.send_message(
                            chat_id=client_chat_id,
                            text="Сообщение отправлено партнеру!\n"
                                 f"Чат: {partner_chat.title}",
                            parse_mode=BASE_PARSE_MODE
                        )

                    """
                    payload = data.get("payload")
                    status = payload.get("status")
                    payment_id = payload.get("paymentId")

                    if status == "completed":
                        await bot.send_message(
                            chat_id=TECHNICAL_COMMAND_CHAT_ID,
                            text=f"payment_id: {payment_id}\n",
                            parse_mode=BASE_PARSE_MODE
                        )
                    """
            except json.JSONDecodeError:
                logging.error("Error decoding JSON message")

        self.consumer.close()


kafka_consumer_manager = KafkaConsumerManager(broker_url=kafka_config.KAFKA_BROKER_URL,
                                              topics=[
                                                  "backend-notifications"
                                              ])
