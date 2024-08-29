from datetime import datetime, timezone
from typing import Any
from typing_extensions import Annotated

from pydantic import BaseModel, Field, model_validator
from pydantic.functional_validators import AfterValidator


def is_past_date(dt: datetime) -> datetime:
    if dt > datetime.now(timezone.utc):
        raise ValueError("datetime should be in the past")
    return dt


# EMM can handle historical searches only
DateTime = Annotated[datetime, AfterValidator(is_past_date)]


class Extraction(BaseModel):
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
    begin: DateTime = Field(description="Data collection start date and time.")
    end: DateTime = Field(description="Data collection end date and time.")

    @model_validator(mode='before')
    @classmethod
    def check_not_equal_datetime(cls, data: Any) -> Any:
        if isinstance(data, dict):
            if data["begin"] == data["end"]:
                raise ValueError("dates cannot be equal")
        return data
