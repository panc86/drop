from datetime import datetime

from app.sources.emm import build_request_url


def test_build_request_url():
    extraction = dict(
        begin=datetime(2024, 9, 5), end=datetime(2024, 9, 6), keywords="test,keyword"
    )
    expected = "https://emm.newsbrief.eu/rss/rss?language=all&type=search&mode=advanced&datefrom=2024-09-05T00%3A00%3A00Z&dateto=2024-09-06T00%3A00%3A00Z&atLeast=test%2Bkeyword&duplicates=false"
    assert build_request_url(extraction) == expected
