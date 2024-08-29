from datetime import datetime, timedelta
import json
from typing import Iterable
from uuid import UUID

from pydantic import BaseModel, ConfigDict, Field


class Extraction(BaseModel):
    tag: str = Field(
        description="Data collection tag for grouping.",
        pattern="[a-zA-Z0-9-_]",
        min_length=3,
        example="place_yyyymmdd",
    )
    keywords: str = Field(
        description="Comma separated list of keywords.",
        min_length=3,
        example="floods,heavy rains",
    )
    description: str | None = Field(
        description="Description of a data collection.", default="example"
    )
    begin: datetime = Field(description="Data collection start date and time.")
    end: datetime = Field(description="Data collection end date and time.")


class ExtractionBuilder(Extraction):
    window_size: timedelta = Field(
        description="Size of time window in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations).",
        default=timedelta(minutes=15),
    )

    def yield_extractions(self) -> Iterable[Extraction]:
        slider = self.begin
        while slider < self.end:
            yield Extraction(
                tag=self.tag,
                keywords=self.keywords,
                description=self.description,
                begin=slider,
                end=slider + self.window_size,
            )
            slider += self.window_size


class ExtractionResponse(Extraction):
    # https://docs.pydantic.dev/latest/concepts/models/#arbitrary-class-instances
    model_config = ConfigDict(from_attributes=True)

    id: UUID
    created_at: datetime
    executed: bool


class DataPoint(BaseModel):
    """Represents a data point model."""

    created_at: str = Field(description="Data point date and time of creation in ISO 8601.")
    id: str = Field(description="Data point identifier.")
    lang: str = Field(description="Data point text language.")
    text: str
    url: str

    def serialize(self):
        return json.dumps(self.model_dump(mode='python'), ensure_ascii=False)
