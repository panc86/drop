import logging
import os
from typing import Iterable

import requests


logger = logging.getLogger(__name__)


# Elasticsearch endpoint
url = os.getenv("ELASTICSEARCH_URL", "http://localhost:9200")


def get_latest_extractions_to_run() -> Iterable[dict[str, str]]:
    query = {
        "query": {
            "bool": {
                "must": [
                    {"term": {"executed": "false"}},
                    {"range": {"end": {"lt": "now"}}},
                ]
            }
        }
    }
    response = requests.get(f"{url}/extractions/_search", json=query)
    return (
        [doc["_source"] for doc in response.json()["hits"]["hits"]]
        if response.status_code == 200
        else []
    )


def update_executed_extraction(extraction_id: str):
    response = requests.post(
        f"{url}/extractions/_update/{extraction_id}", json={"doc": {"executed": "true"}}
    )
    return response.json()
