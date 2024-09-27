from datetime import datetime
from typing import Any, Iterable
import urllib.parse

import pandas


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


def download_data(url: str) -> Iterable[dict[str, Any]]:
    try:
        xml_data = pandas.read_xml(url, parser="etree", xpath=".//item")
    except ValueError:
        print(url)
        return []
    else:
        yield from xml_data.to_dict(orient="records")


def yield_data_points(extraction: dict) -> Iterable[dict[str, Any]]:
    for data_point in download_data(build_request_url(extraction)):
        yield dict(
            extraction=extraction,
            created_at=datetime.strptime(
                data_point["pubDate"], "%a, %d %b %Y %H:%M:%S %z"
            ),
            id=data_point["guid"],
            text=data_point["title"],
            url=data_point["link"],
            source="emm",
        )
