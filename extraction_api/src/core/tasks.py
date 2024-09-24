import os

from redis import Redis
from rq import Queue
from rq.job import Job

from core.producer import publish_events
from core.sources import emm


IS_DOCKER_ENV = os.path.exists("/.dockerenv")

# message broker
redis = Redis(host="redis" if IS_DOCKER_ENV else "localhost", port=6379, db=0)
# default queue
task_queue = Queue(connection=redis)


def report_job_failure(job, connection, type, value, traceback):
    print(dict(job_id=job.id, job_description=job.description, errors=value))


def extract_data_points_from_sources(extraction):
    data_points = emm.yield_data_points(extraction)
    publish_events([extraction], "extractions")
    publish_events(data_points, "raw_texts")


def add_extraction_to_task_queue(extraction: dict) -> Job:
    return task_queue.enqueue(
        extract_data_points_from_sources,
        args=(extraction, ),
        on_failure=report_job_failure,
        job_timeout="3m",
    )
