from datetime import datetime
from typing import Any, Iterable
import urllib.parse

import pandas


class EMMSourcingError(Exception):
    pass


def build_request_url(extraction: dict) -> str:
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    url = "https://emm.newsbrief.eu/rss/rss?{params}"
    return url.format(
        params=urllib.parse.urlencode(
            dict(
                language="all",
                type="search",
                mode="advanced",
                datefrom=extraction["begin"].strftime(date_format),
                dateto=extraction["end"].strftime(date_format),
                atLeast=extraction["keywords"].replace(",", "+"),
                duplicates="false",
            )
        )
    )


def download_events(url: str) -> Iterable[dict[str, Any]]:
    try:
        events = pandas.read_xml(url, parser="etree", xpath=".//item")
    except ValueError:
        raise EMMSourcingError(f"failed to download events from {url}")
    else:
        yield from events.to_dict(orient="records")


def yield_events(extraction: dict) -> Iterable[dict[str, Any]]:
    for event in download_events(build_request_url(extraction)):
        yield dict(
            extraction=extraction,
            created_at=datetime.strptime(
                event["pubDate"], "%a, %d %b %Y %H:%M:%S %z"
            ),
            id=event["guid"],
            text=event["title"],
            url=event["link"],
            source="emm",
        )
