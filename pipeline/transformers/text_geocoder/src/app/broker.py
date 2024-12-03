from datetime import datetime
import json
import logging
import os
from typing import Any

from confluent_kafka import Consumer, Producer


logger = logging.getLogger(__name__)

bootstrap_servers = os.environ.get("KAFKA_BOOTSTRAP_SERVERS", "localhost:9092")


def json_serial(obj: Any):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError(f"Type {type(obj)} not serializable")


def serialize_event(event: dict) -> bytes:
    return json.dumps(event, ensure_ascii=False, default=json_serial).encode("utf-8")


def log_events(events):
    producer = Producer({
        "bootstrap.servers": bootstrap_servers,
        "acks": "all",
    })
    def delivery_callback(error, event):
        msg = dict(
            topic=event.topic(), event=json.loads(event.value()), error=error
        )
        if error is not None:
            logger.error(msg)
        logger.debug(msg)
    for event in events:
        producer.produce(
            topic="geocoded_texts",
            value=serialize_event(event),
            callback=delivery_callback,
        )
    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


def consume_batched_events():
    logger.info("listening for incoming events...")
    consumer = Consumer({
        "bootstrap.servers": bootstrap_servers,
        "group.id": "geocoding",
        "auto.offset.reset": "earliest",
    })
    consumer.subscribe(["annotated_texts"])
    # model prediction is computationally expensive and should be executed in batches
    batch = []
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if len(batch) > 0:
                    yield batch
                    logger.debug(f"processed {len(batch)} events...")
                    batch = []
            elif msg.error():
                logger.error(msg.error())
            else:
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 256:
                    yield batch
                    logging.debug(f"processed {len(batch)} events...")
                    batch = []
    except KeyboardInterrupt:
        print()
        logger.info("Interrupted")
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
