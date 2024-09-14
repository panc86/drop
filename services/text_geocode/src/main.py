import warnings

from fastapi import FastAPI, status

from geocode import config
from geocode.gazetteer import load_gazetteer
from geocode.models import load_bert_model
from geocode.tags import parse_location_tags, titlecase, match_geo_political_entities

# ignore warnings
warnings.filterwarnings("ignore")

# initialize components
bert_model = load_bert_model()
gazetteer = load_gazetteer(config.gazetteer_filepath)
# initialize API router app
app = FastAPI(**config.api_config)


@app.get("/ping/")
def ping():
    """An health check endpoint that returns pong."""
    return "pong"


@app.post(
    "/geocode/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Geocode texts",
)
async def geocode_texts(texts: list[str]):
    tags = parse_location_tags(*bert_model(titlecase(texts)))
    matches = match_geo_political_entities(tags, gazetteer)
    return dict(texts=texts, tags=tags, matches=matches)

