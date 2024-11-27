import json
import os
import logging
from typing import Iterable

from confluent_kafka import Consumer, Producer


IS_DOCKER_ENV = os.path.exists("/.dockerenv")
KAFKA_BROKER_URL = os.environ.get(
    "KAFKA_BROKER_URL", "broker:29092" if IS_DOCKER_ENV else "localhost:9092"
)


def log_events(events: Iterable[bytes], topic: str = "events"):
    producer = Producer(
        {
            "bootstrap.servers": KAFKA_BROKER_URL,
            "acks": "all",
        }
    )

    def delivery_callback(error, event):
        msg = dict(
            topic=event.topic(), event=json.loads(event.value()), error=error
        )
        if error is not None:
            logging.error(msg)
        logging.debug(msg)

    for event in events:
        producer.produce(topic=topic, value=event, callback=delivery_callback)
    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


def listen_for_incoming_extractions() -> Iterable[dict]:
    logging.info("listening for incoming extractions...")
    consumer = Consumer(
        {
            "bootstrap.servers": KAFKA_BROKER_URL,
            "group.id": "extractors",
            "auto.offset.reset": "earliest",
        }
    )
    try:
        consumer.subscribe(["extractions"])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                logging.error(msg.error())
            else:
                yield json.loads(msg.value())
    except KeyboardInterrupt:
        print()
        logging.warning("Interrupted")
    finally:
        # Leave group and commit final offsets
        consumer.close()
