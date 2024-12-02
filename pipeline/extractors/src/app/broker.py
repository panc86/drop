import json
import os
import logging
from typing import Iterable

from confluent_kafka import Consumer, Producer


logger = logging.getLogger(__name__)
bootstrap_servers = f'{os.environ.get("KAFKA_BROKER_HOST", "localhost")}:9092'


def log_events(events: Iterable[bytes]):
    producer = Producer(
        {
            "bootstrap.servers": bootstrap_servers,
            "acks": "all",
        }
    )

    def delivery_callback(error, event):
        msg = dict(
            topic=event.topic(), event=json.loads(event.value()), error=error
        )
        if error is not None:
            logger.error(msg)
        logger.debug(msg)

    for event in events:
        producer.produce(topic="events", value=event, callback=delivery_callback)
    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


def listen_for_incoming_extractions() -> Iterable[dict]:
    logger.info("listening for incoming extractions...")
    consumer = Consumer(
        {
            "bootstrap.servers": bootstrap_servers,
            "group.id": "extractors",
            "auto.offset.reset": "earliest",
        }
    )
    consumer.subscribe(["extractions"])
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                pass
            elif msg.error():
                logger.error(msg.error())
            else:
                yield json.loads(msg.value())
    except KeyboardInterrupt:
        print()
        logger.warning("Interrupted")
    finally:
        # Leave group and commit final offsets
        consumer.close()
