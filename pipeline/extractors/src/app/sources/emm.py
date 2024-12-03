from datetime import datetime
from typing import Iterable
import logging

from urllib.parse import urlencode
from xml.etree import ElementTree

import requests


logger = logging.getLogger(__name__)


def build_request_url(extraction: dict) -> str:
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    url = "https://emm.newsbrief.eu/rss/rss?{params}"
    return url.format(
        params=urlencode(
            dict(
                language="all",
                type="search",
                mode="advanced",
                datefrom=datetime.fromisoformat(extraction["begin"]).strftime(date_format),
                dateto=datetime.fromisoformat(extraction["end"]).strftime(date_format),
                atLeast=extraction["keywords"].replace(",", "+") if extraction["keywords"] else "",
                duplicates="false",
            )
        )
    )


def download_xml_data(url: str) -> requests.Response:
    return requests.get(url)


def parse_articles(articles: bytes) -> Iterable[dict]:
    root = ElementTree.fromstring(articles)
    for item in root.findall("./channel/item"):
        yield dict(
            created_at=datetime.strptime(
                item.find("pubDate").text, "%a, %d %b %Y %H:%M:%S %z"
            ),
            text=item.find("title").text,
            url=item.find("link").text,
            id=item.find("guid").text,
        )


class EMM:
    def fetch_data(self, extraction: dict) -> Iterable[dict]:
        response = download_xml_data(build_request_url(extraction))
        if response.status_code != 200:
            logger.error(
                dict(extraction=extraction, error=response.reason, url=response.url)
            )
            return
        for article in parse_articles(response.content):
            yield dict(
                **article, metadata=dict(extraction=extraction, source="emm")
            )
