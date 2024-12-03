import logging
import os

import redis
import rq

from app import broker, events


logger = logging.getLogger(__name__)


db = redis.from_url(os.environ.get("REDIS_URL", "redis://"))
queue = rq.Queue(connection=db)
worker = rq.Worker([queue], connection=db)


def report_job_failure(job, connection, type, value, traceback):
    logger.error(dict(job=dict(id=job.id, args=job.args), error=dict(type=type, value=value)))


def extract_events_job(extraction: dict):
    broker.log_events(events.fetch_events(extraction))


def enqueue_job(extraction: dict) -> rq.job.Job:
    return queue.enqueue(
        extract_events_job,
        args=(extraction,),
        on_failure=report_job_failure,
        job_timeout="30s",
    )
