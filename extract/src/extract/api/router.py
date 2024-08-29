from fastapi import FastAPI, Depends, status
from sqlalchemy.orm import Session

from extract.api.config import APIConfig
from extract.db.core import get_db
from extract.db.crud import create_extraction, read_extractions
from extract.db.schemas import ExtractionBuilder, ExtractionResponse


# initialize API router app
app = FastAPI(**APIConfig().model_dump())


@app.get("/ping/")
def ping():
    """An health check endpoint that returns pong."""
    return "pong"


@app.get(
    "/extractions/",
    response_model=list[ExtractionResponse],
    status_code=status.HTTP_200_OK,
    summary="Read available extraction metadata",
)
async def get_extraction_metadata(db: Session = Depends(get_db)):
    return list(map(ExtractionResponse.model_validate, read_extractions(db)))


@app.post(
    "/extraction/",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Fires extraction metadata request",
)
async def create_extraction_metadata(
    builder: ExtractionBuilder,
    db: Session = Depends(get_db)
):
    for extraction in builder.yield_extractions():
        create_extraction(db, extraction)
    return dict(success=True, error=None)
