from datetime import datetime, timedelta, timezone
from typing import Any, Iterable
from typing_extensions import Self

from uuid import UUID, uuid4

from pydantic import BaseModel, Field, model_validator


class ExtractionBase(BaseModel):
    tag: str = Field(
        description="Data collection tag for grouping.",
        pattern="[a-zA-Z0-9-_]",
        min_length=3,
        examples=["flood_lombardia_20240914"],
    )
    keywords: str = Field(
        description="Comma separated list of keywords.",
        min_length=3,
        examples=["Lombardia,Milano,Varese"],
    )
    begin: datetime = Field(description="Data collection start date and time.")
    end: datetime = Field(description="Data collection end date and time.")

    @model_validator(mode='after')
    def check_begin_end_dates_not_equal(self) -> Self:
        if self.begin == self.end:
            raise ValueError('begin and end cannot be equal')
        return self


class Extraction(ExtractionBase):
    id: UUID
    created_at: datetime
    executed: bool

    def to_json(self) -> dict[str, Any]:
        return dict(
            id=str(self.id),
            created_at=self.created_at.isoformat(),
            executed=self.executed,
            tag=self.tag,
            keywords=self.keywords,
            begin=self.begin.isoformat(),
            end=self.end.isoformat()
        )


class ExtractionBuilder(ExtractionBase):
    window_size: timedelta = Field(
        description="Size of time window in [ISO 8601](https://en.wikipedia.org/wiki/ISO_8601#Durations).",
        default=timedelta(minutes=15),
    )

    def yield_extractions(self) -> Iterable[Extraction]:
        slider = self.begin
        while slider < self.end:
            yield Extraction(
                id=uuid4(), # TODO: make it consistent e.g. tag+begin+end
                created_at=datetime.now(timezone.utc),
                executed=False,
                tag=self.tag,
                keywords=self.keywords,
                begin=slider,
                end=slider + self.window_size,
            )
            slider += self.window_size
