from datetime import datetime, timezone
from sqlalchemy import and_, not_
from sqlalchemy.orm import Session

from extract.db import models, schemas


def create_extraction(db: Session, schema: schemas.Extraction) -> models.Extraction:
    extraction = models.Extraction(**schema.model_dump())
    db.add(extraction)
    db.commit()
    db.refresh(extraction)
    return extraction


def read_extractions(db: Session) -> list[models.Extraction]:
    # disregard future extrations and extractions already executed
    return db.query(models.Extraction).filter(
        and_(
            not_(models.Extraction.executed),
            models.Extraction.end <= datetime.now(timezone.utc)
        )
    ).all()
