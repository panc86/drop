import json
import os

from redis import Redis
from rq import Queue
from rq.job import Job
from rq.exceptions import NoSuchJobError

from api.producer import publish_events
from api.sources import emm


IS_DOCKER_ENV = os.path.exists("/.dockerenv")

# message broker
redis = Redis(host="redis" if IS_DOCKER_ENV else "localhost", port=6379, db=0)
# default queue
work_queue = Queue(connection=redis)


def report_job_failure(job, connection, type, value, traceback):
    with open("/var/log/error.log", "a") as log:
        log.write(json.dumps(dict(id=job.id, args=job.args, errors=value), ensure_ascii=False, default=str)+"\n")


def get_job(id: str) -> Job | None:
    try:
        return Job.fetch(id, connection=redis)
    except NoSuchJobError:
        pass


def extract_events_from_sources(extraction: dict):
    publish_events(emm.yield_events(extraction), "raw_texts")


def to_work_queue(extraction: dict) -> Job:
    return work_queue.enqueue_at(
        extraction["end"],
        extract_events_from_sources,
        args=(extraction, ),
        on_failure=report_job_failure,
        job_timeout="1m",
    )
