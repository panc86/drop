from flask import Flask, request
from pydantic import ValidationError

from core import models
from core.producer import publish_events
from core.sources import emm


app = Flask(__name__)


@app.route("/", methods=["GET"])
def home():
    return "Extraction API for Disaster Risk Observability Platform (DROP)"


@app.route("/ping/", methods=["GET"])
def ping_api():
    return "pong"


@app.route("/emm/", methods=["POST"])
def stream_data_points():
    try:
        extraction = dict(models.Extraction(**request.json))
    except ValidationError as error:
        return error.json(), 400
    else:
        publish_events(extraction, "extractions")
        publish_events(emm.yield_data_points(extraction), "raw_texts")
    return extraction
