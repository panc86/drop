from fastapi import APIRouter, HTTPException, status

from api import models, database


app = APIRouter()


@app.get("/ping/")
def ping():
    """An health check endpoint that returns pong."""
    return "pong"


@app.post(
    "/extraction/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Fires extraction metadata request",
)
async def create_extraction_requests(builder: models.ExtractionBuilder):
    if not database.is_ready():
        raise HTTPException(status_code=500, detail="DB not ready")
    return database.upload_data(
        database.build_payload(
            [extraction.to_json() for extraction in builder.yield_extractions()],
        )
    )
