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
    print(dict(id=job.id, args=job.args, errors=value))


def get_job(id: str) -> Job | None:
    try:
        return Job.fetch(id, connection=redis)
    except NoSuchJobError:
        pass


def extract_data_points_from_sources(extraction: dict):
    data_points = emm.yield_data_points(extraction)
    publish_events([extraction], "extractions")
    publish_events(data_points, "raw_texts")


def to_work_queue(extraction: dict) -> Job:
    return work_queue.enqueue(
        extract_data_points_from_sources,
        args=(extraction, ),
        on_failure=report_job_failure,
        job_timeout="3m",
    )
