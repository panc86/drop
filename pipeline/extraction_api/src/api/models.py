from datetime import datetime

from pydantic import BaseModel, Field, model_validator


class Extraction(BaseModel):
    """Represents the payload of an extraction request."""

    tag: str = Field(
        description="Data collection tag for grouping.",
        pattern="[a-zA-Z0-9-_]",
        min_length=3,
        examples=["flood_lombardia_20240914"],
    )
    keywords: str = Field(
        description="Comma separated list of keywords.\nEmpty string disables keywords filter.",
        examples=["Lombardia,Milano,Varese"],
    )
    begin: datetime = Field(description="Extraction start date and time in ISO 8601.")
    end: datetime = Field(description="Extraction end date and time in ISO 8601.")

    meta: dict | None = Field(description="Extraction metadata.")

    @model_validator(mode='before')
    @classmethod
    def begin_lt_end(cls, data: dict) -> dict:
        """Begin is lower than end."""
        if isinstance(data, dict):
            if data["begin"] >= data["end"]:
                raise ValueError("begin must be lower than end.")
            return data
