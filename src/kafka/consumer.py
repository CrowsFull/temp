import asyncio
import json
import logging
from typing import List

from confluent_kafka import Consumer, KafkaError
from telegram import Bot

from bot.handlers.consts.consts import BASE_PARSE_MODE
from config.kafka import kafka_config
from kafka.enums import KafkaTopic, NotificationType
from kafka.handlers import send_status_message
from kafka.utils.enums import Status


class KafkaConsumerManager:

    def __init__(self, broker_url: str, topics: List[str]):
        self.consumer_conf: dict = {
            'bootstrap.servers': broker_url,
            'group.id': 'telegram_bot_group',
            'auto.offset.reset': 'latest'
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
                    message = msg.value().decode('utf-8')
                    data = json.loads(message)

                    tpe = data.get("tpe")
                    payload = data.get("payload")

                    if tpe == NotificationType.PAYMENT_STATUS_CHANGED:
                        await send_status_message(bot, payload)
                        await asyncio.sleep(2)
            except json.JSONDecodeError:
                logging.error("Error decoding JSON message")

        self.consumer.close()


kafka_consumer_manager = KafkaConsumerManager(broker_url=kafka_config.KAFKA_BROKER_URL,
                                              topics=[
                                                  "backend-notifications"
                                              ])
