from datetime import datetime
import json
import os
from typing import Any
import warnings

from confluent_kafka import Consumer, Producer

from core import geocoder

# ignore warnings
warnings.filterwarnings("ignore")


KAFKA_BROKER_URL = os.environ.get("KAFKA_BROKER_URL", "localhost:9092")


def json_serial(obj: Any):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, datetime):
        return obj.isoformat()
    raise TypeError("Type %s not serializable" % type(obj))


def serialize_event(event: dict) -> bytes:
    return json.dumps(event, ensure_ascii=False, default=json_serial).encode("utf-8")


def delivery_callback(error, event):
    print(dict(topic=event.topic(), event=event.value(), error=error))


def publish_geocoded_events(events, topic: str = "geocoded_texts"):
    producer = Producer({
        "bootstrap.servers": KAFKA_BROKER_URL,
        "acks": "all",
    })
    for event in events:
        producer.produce(
            topic=topic,
            value=serialize_event(event),
            callback=delivery_callback,
        )
    # Block until the messages are sent.
    producer.poll(10000)
    producer.flush()


def consume_raw_events():
    consumer = Consumer({
    "bootstrap.servers": KAFKA_BROKER_URL,
    "group.id": "geocode",
    "auto.offset.reset": "earliest",
})
    # model prediction is computationally expensive and should be executed in batches
    model = geocoder.get_model()
    batch = []
    try:
        consumer.subscribe(["annotated_texts"])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if len(batch) > 0:
                    publish_geocoded_events(model(batch))
                    print(f"processed {len(batch)} events...")
                    batch = []
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 256:
                    publish_geocoded_events(model(batch))
                    print(f"processed {len(batch)} events...")
                    batch = []
    except KeyboardInterrupt:
        print("\nInterrupted")
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


if __name__ == '__main__':
    import sys
    args = sys.argv[:1]
    if args and args[0] == "--probe":
        probes = [dict(text="probe test no {}".format(n), annotation=dict(impact=0.64, flood=0.87)) for n in range(10)]
        publish_geocoded_events(probes, "annotated_texts")
    consume_raw_events()
