from flask import Flask, request
from pydantic import ValidationError

from api import models, worker


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Extraction API for Disaster Risk Observability Platform (DROP)", 200


@app.route("/ping/", methods=["GET"])
def ping_api():
    return "pong", 200


@app.route("/jobs/<job_id>", methods=["GET"])
def get_job(job_id: str):
    job = worker.get_job(job_id)
    if not job:
        return job_id, 404
    return dict(
        id=job.id,
        args=job.args,
        status=job.get_status(refresh=True),
        error=job.exc_info,
        last_update=job.last_heartbeat,
    ), 200


@app.route("/emm/", methods=["POST"])
def stream_events():
    try:
        extraction = dict(models.Extraction(**request.json))
    except ValidationError as error:
        return error.json(), 400
    else:
        job = worker.to_work_queue(extraction)
        return dict(extraction=extraction, task_url=f"/jobs/{job.id}"), 202
