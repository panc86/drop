import json
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional, Iterable, Protocol
from uuid import UUID, uuid4

from app.sources.emm import EMM


def json_serializer(value: Any):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(value, datetime):
        return value.isoformat()
    if isinstance(value, UUID):
        return str(value)
    raise TypeError(f"Type {type(value)} not serializable")


def to_bytes(data: dict) -> bytes:
    return json.dumps(data, ensure_ascii=False, default=json_serializer).encode("utf-8")


@dataclass
class Event:
    """Represents an event from a data source."""

    created_at: datetime
    text: str
    url: str
    metadata: Optional[dict]
    id: Optional[UUID] = field(default_factory=uuid4)

    def serialize(self) -> bytes:
        return to_bytes(self.__dict__)


class Source(Protocol):
    def fetch_data(self, extraction: dict) -> Iterable[dict]: ...


# list of available data sources
sources: list[Source] = [EMM(),]


def fetch_events(extraction: dict) -> Iterable[bytes]:
    for source in sources:
        for data in source.fetch_data(extraction):
            yield Event(**data).serialize()
