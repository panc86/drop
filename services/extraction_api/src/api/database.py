import json
import os
from typing import Any, Iterable

import requests


url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")
headers = {"Content-Type": "application/x-ndjson"}


def build_payload(data: Iterable[dict[str, Any]]) -> str:
    payload = ""
    for row in data:
        payload += json.dumps({"index": {"_id": row["id"]}}) + "\n"
        payload += json.dumps(row, ensure_ascii=False) + "\n"
    return payload


def upload_data(payload: str) -> dict[str, Any]:
    response = requests.post(f"{url}/extractions/_bulk", headers=headers, data=payload)
    if response.status_code == 200:
        return response.json()
    return dict(status_code=response.status_code, message=response.content)


def is_ready() -> bool:
    try:
        return requests.get(url).status_code == 200
    except requests.exceptions.ConnectionError:
        return False
