from datetime import datetime
import json
import os
from typing import Any, Iterable

from confluent_kafka import Producer


default_config = {
    # User-specific properties that you must set
    "bootstrap.servers": os.environ.get("KAFKA_BROKER_URL", "localhost:9092"),
    # Fixed properties
    "acks": "all",
}


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def serialize_event(event: dict) -> bytes:
    return json.dumps(event, ensure_ascii=False, default=json_serial).encode(
                "utf-8"
            )


def publish_events(events: Iterable[dict[str, Any]], topic: str, config: dict = default_config):
    producer = Producer(config)
    # Optional per-message delivery callback (triggered by poll() or flush())
    # when a message has been successfully delivered or permanently
    # failed delivery (after retries).
    def delivery_callback(error, event):
        print(dict(topic=event.topic(), event=event.value(), error=error))

    for event in events:
        producer.produce(
            topic=topic,
            value=serialize_event(event),
            callback=delivery_callback,
        )

    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()
