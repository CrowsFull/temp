from confluent_kafka import Producer
import json
import random
import time

KAFKA_BROKER_URL = "localhost:9092"
TOPIC_NAME = "backend-notifications"

producer_conf = {
    'bootstrap.servers': KAFKA_BROKER_URL
}

# Инициализация продьюсера
producer = Producer(producer_conf)


def delivery_report(err, msg):
    """Сообщает о статусе доставки сообщения"""
    if err is not None:
        print(f"Ошибка доставки: {err}")
    else:
        print(f"Сообщение доставлено в {msg.topic()} [партия {msg.partition()}]")


def send_random_status_update():
    status = random.choice(["pending", "finished", "started"])

    message = {
        "partner_chat_id": -4504066274,
        "client_chat_id": -4518899699,
        "project": "FB55.20",
        "status": status,
        "price": random.randint(-10000, 100000),
        "link": "https://tronscan.org/#/transaction/01682e90a17f77aa953db240cb467c6f8df0f23222fd7165e6217b32639daf7b"
    }

    producer.produce(
        TOPIC_NAME,
        value=json.dumps(message).encode('utf-8'),
        callback=delivery_report
    )

    producer.flush()


if __name__ == "__main__":
    while True:
        send_random_status_update()
        time.sleep(10)
