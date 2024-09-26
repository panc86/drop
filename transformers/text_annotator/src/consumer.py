import json
import os

from confluent_kafka import Consumer

from producer import publish_events


IS_DOCKER_ENV = os.path.exists("/.dockerenv")


default_config = {
    # User-specific properties that you must set
    "bootstrap.servers": "broker:29092" if IS_DOCKER_ENV else "localhost:9092",
    # Fixed properties
    "group.id": "annotation",
    "auto.offset.reset": "earliest",
}


def consume_events(topics: list[str], handler, config: dict = default_config):
    consumer = Consumer(config)
    # model prediction is computationally expensive and should be executed in batches
    batch = []
    try:
        consumer.subscribe(topics)
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if len(batch) > 0:
                    publish_events(handler(batch), "annotated_texts")
                    print(f"processed {len(batch)} events...")
                    batch = []
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 256:
                    publish_events(handler(batch), "annotated_texts")
                    print(f"processed {len(batch)} events...")
                    batch = []
    except KeyboardInterrupt:
        print("\nInterrupted")
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
