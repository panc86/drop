import json
import os
from typing import Any, Iterable

import requests

from confluent_kafka import Consumer


default_config = {
    # User-specific properties that you must set
    "bootstrap.servers": os.getenv("BROKER_URL", "localhost:9092"),
    # Fixed properties
    "group.id": "products",
    "auto.offset.reset": "earliest",
}


url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")


def is_alive() -> bool:
    return requests.get(url).status_code == 200


def build_payload(data: Iterable[dict[str, Any]]) -> str:
    payload = ""
    for row in data:
        payload += json.dumps({"index": {"_id": row["id"]}}) + "\n"
        payload += json.dumps(row, ensure_ascii=False) + "\n"
    return payload


def upload_data(payload: str) -> dict[str, Any]:
    headers = {"Content-Type": "application/x-ndjson"}
    response = requests.post(f"{url}/events/_bulk", headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    return dict(status_code=response.status_code, message=response.content)


def consume_events(topics: list[str], config: dict = default_config):
    consumer = Consumer(config)
    # model prediction is computationally expensive and should be executed in batches
    batch = []
    try:
        consumer.subscribe(topics)
        while True:
            msg = consumer.poll(1.0)
            if msg is None:
                if len(batch) > 0:
                    upload_data(build_payload(batch))
                    print(f"processed {len(batch)} events...")
                    batch = []
            elif msg.error():
                print("ERROR: {}".format(msg.error()))
            else:
                # print(dict(topic=msg.topic(), key=msg.key().decode('utf-8'), value=msg.value().decode('utf-8')))
                batch.append(json.loads(msg.value().decode("utf-8")))
                if len(batch) == 256:
                    upload_data(build_payload(batch))
                    print(f"processed {len(batch)} events...")
                    batch = []
    except KeyboardInterrupt:
        print("\nInterrupted")
        pass
    finally:
        # Leave group and commit final offsets
        consumer.close()


if __name__ == "__main__":
    if is_alive():
        consume_events(["geocoded_texts"])
    else:
        print("not ready")
