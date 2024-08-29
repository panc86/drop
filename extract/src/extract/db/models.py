from datetime import datetime, timezone
from uuid import uuid4

from sqlalchemy import Boolean, Column, TIMESTAMP, String, UUID
from sqlalchemy.ext.declarative import declarative_base


Base = declarative_base()


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Extraction(Base):
    __tablename__ = "extractions"

    id = Column(UUID, default=uuid4, primary_key=True)
    created_at = Column(TIMESTAMP, default=utcnow)
    tag = Column(String, index=True)
    keywords = Column(String)
    description = Column(String)
    begin = Column(TIMESTAMP)
    end = Column(TIMESTAMP)
    executed = Column(Boolean, default=False)

    def __repr__(self) -> str:
        return f"Extraction(id={self.id}, created_at={self.created_at}, tag={self.tag}), begin={self.begin}, end={self.end}"
