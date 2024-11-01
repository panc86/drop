from datetime import datetime, timedelta, timezone

from pydantic import ValidationError
import pytest

from api.models import Extraction


def test_valid_extraction_is_created_successfully():
    result = Extraction(**{
        "tag": "test",
        "keywords": "test-keyword",
        "begin": datetime(2024, 9, 5, tzinfo=timezone.utc),
        "end": datetime(2024, 9, 5, 23, 23, 59, tzinfo=timezone.utc),
    })
    assert isinstance(result, Extraction)


def test_extraction_with_invalid_begin_fails():
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        Extraction(**{
            "tag": "test",
            "keywords": "test-keyword",
            "begin": now,
            "end": now+timedelta(seconds=5),
        })


def test_extraction_with_equal_begin_and_end_datetimes_fails():
    now = datetime.now(timezone.utc)
    with pytest.raises(ValidationError):
        Extraction(**{
            "tag": "test",
            "keywords": "test-keyword",
            "begin": now+timedelta(seconds=5),
            "end": now,
        })


def test_extraction_keywords_null_is_not_allowed():
    with pytest.raises(ValidationError):
        Extraction(**{
            "tag": "test",
            "keywords": None,
            "begin": datetime(2024, 9, 5, tzinfo=timezone.utc),
            "end": datetime(2024, 9, 5, 23, 23, 59, tzinfo=timezone.utc),
        })
