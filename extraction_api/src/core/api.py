from flask import Flask, request
from pydantic import ValidationError

from core import models
from core.tasks import add_extraction_to_task_queue


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Extraction API for Disaster Risk Observability Platform (DROP)", 200


@app.route("/ping/", methods=["GET"])
def ping_api():
    return "pong", 200


@app.route("/emm/", methods=["POST"])
def stream_data_points():
    try:
        extraction = dict(models.Extraction(**request.json))
    except ValidationError as error:
        return error.json(), 400
    else:
        job = add_extraction_to_task_queue(extraction)
        return dict(job_id=job.id, extraction=extraction), 201
