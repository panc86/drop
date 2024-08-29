import logging
import os
import time
from typing import Iterable

import redis

from extract.db.core import get_db
from extract.db.crud import read_extractions
from extract.sources import emm


logger = logging.getLogger(__name__)

# initialize message broker
broker = redis.from_url(os.getenv("BROKER_URL", "redis://"))


def send_to_pipeline(messages: Iterable[str]):
    for message in messages:
        broker.publish("transformer", message)
        logger.debug(message)


def extract_from_source(source):
    for db in get_db():
        for extraction in read_extractions(db):
            send_to_pipeline(source.extract_data(extraction))
            extraction.executed = True
        db.commit()


def run():
    logger.info("run extraction service...")
    while True:
        extract_from_source(emm)
        time.sleep(60)
