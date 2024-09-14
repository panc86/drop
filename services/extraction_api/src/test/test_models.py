from datetime import datetime, timezone
from uuid import UUID

import pytest

from api.models import Extraction


@pytest.fixture(scope="module")
def extraction():
    return Extraction(**{
        "id": UUID("4e5adf30-fefa-4a20-93a0-73512c71c4b6"),
        "created_at": datetime(2024, 9, 5, tzinfo=timezone.utc),
        "executed": False,
        "tag": "test",
        "keywords": "test-keyword",
        "description": "a test extraction",
        "begin": datetime(2024, 9, 5, tzinfo=timezone.utc),
        "end": datetime(2024, 9, 5, 23, 23, 59, tzinfo=timezone.utc),
    })
