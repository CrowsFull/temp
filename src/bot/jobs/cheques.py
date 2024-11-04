import logging

import telegram.ext

from kafka.consumer import kafka_consumer_manager


async def handle_message_queue(context: telegram.ext.CallbackContext):
    logging.info("Bot started waiting for messages.")
    await kafka_consumer_manager.handle_kafka_messages(context.bot)
    logging.info("Bot finished waiting for messages.")
