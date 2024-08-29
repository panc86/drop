import json
import os

from confluent_kafka import Consumer

from producer import publish_events


IS_DOCKER_ENV = os.path.exists("/.dockerenv")


default_config = {
    # User-specific properties that you must set
    "bootstrap.servers": "broker:29092" if IS_DOCKER_ENV else "localhost:9092",
    # Fixed properties
    "group.id": "data_point_group",
    "auto.offset.reset": "earliest",
}


def consume_events(topics: list[str], handler, config: dict = default_config):
    outgoing_topic = "annotated_texts"
    consumer = Consumer(config)
    consumer.subscribe(topics)
    # model prediction is computationally expensive and should be executed in batches
    batch = []
    try:
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                # Initial message consumption may take up to
                # `session.timeout.ms` for the consumer group to
                # rebalance and start consuming
                if len(batch) > 0:
                    print("executes batch leftover...")
                    publish_events(handler(batch), outgoing_topic)
                    batch = []
                print("Waiting...")
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                # print(dict(topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 32:
                    publish_events(handler(batch), outgoing_topic)
                    batch = []
    except KeyboardInterrupt:
        print("\nInterrupted")
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()
