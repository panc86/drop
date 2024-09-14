from fastapi import FastAPI, status

from annotation import config
from annotation.cleaner import clean_texts
from annotation.models import annotate, vectorize


# initialize API router app
app = FastAPI(**config.api_config)


@app.get("/ping/")
def ping():
    """An health check endpoint that returns pong."""
    return "pong"


@app.post(
    "/annotate/",
    response_model=dict,
    status_code=status.HTTP_200_OK,
    summary="Annotate texts",
)
async def annotate_texts(texts: list[str]):
    return dict(texts=texts, **annotate(vectorize(clean_texts(texts))))
