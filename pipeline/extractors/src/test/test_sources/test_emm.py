from app.sources.emm import build_request_url


def test_build_request_url():
    extraction = dict(
        begin="2024-09-05", end="2024-09-06", keywords="test,keyword"
    )
    expected = "https://emm.newsbrief.eu/rss/rss?language=all&type=search&mode=advanced&datefrom=2024-09-05T00%3A00%3A00Z&dateto=2024-09-06T00%3A00%3A00Z&atLeast=test%2Bkeyword&duplicates=false"
    assert build_request_url(extraction) == expected
