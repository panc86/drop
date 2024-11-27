from datetime import datetime
import json
import os
from typing import Any

from confluent_kafka import Consumer, Producer

from core import annotator


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


def publish_annotated_events(events, topic: str = "annotated_texts"):
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
    "group.id": "annotation",
    "auto.offset.reset": "earliest",
})
    # model prediction is computationally expensive and should be executed in batches
    model = annotator.get_model()
    batch = []
    try:
        consumer.subscribe(["events"])
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if len(batch) > 0:
                    publish_annotated_events(model(batch))
                    print(f"processed {len(batch)} events...")
                    batch = []
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 256:
                    publish_annotated_events(model(batch))
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
        probes = [dict(id=n * 100, text="probe test no {}".format(n)) for n in range(10)]
        publish_annotated_events(probes, "raw_texts")
    consume_raw_events()
