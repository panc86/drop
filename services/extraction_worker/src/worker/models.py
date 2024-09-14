from dataclasses import dataclass
from datetime import datetime


@dataclass
class DataPoint:
    """Represents a data point model."""

    created_at: datetime
    id: str
    lang: str
    text: str
    url: str
    source: str

    def to_json(self):
        return dict(
            created_at=self.created_at.isoformat(),
            id=self.id,
            lang=self.lang,
            text=self.text,
            url=self.url,
            source=self.source,
        )

