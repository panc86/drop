from datetime import datetime
import logging
from typing import Any, Iterable
import pandas
import urllib.parse

from extract.db import models, schemas


logger = logging.getLogger(__name__)


def build_request_url(extraction: models.Extraction) -> str:
    date_format = "%Y-%m-%dT%H:%M:%SZ"
    url = "https://emm.newsbrief.eu/rss/rss?{params}"
    return url.format(
        params=urllib.parse.urlencode(
            dict(
                language="all",
                type="search",
                mode="advanced",
                datefrom=extraction.begin.strftime(date_format),
                dateto=extraction.end.strftime(date_format),
                atLeast=extraction.keywords.replace(",", "+"),
                duplicates="false",
            )
        )
    )


def download_xml_data(url: str) -> Iterable[dict[str, Any]]:
    try:
        logger.debug(url)
        return pandas.read_xml(url, parser="etree", xpath=".//item").to_dict(orient="records")
    except ValueError as error:
        logger.error(dict(url=url, error=error))
        return []


def convert_data(entry: dict) -> str:
    return schemas.DataPoint(
        created_at=datetime.strptime(entry["pubDate"], "%a, %d %b %Y %H:%M:%S %z").isoformat(),
        id=entry["guid"],
        lang=entry["language"],
        text=entry["title"],
        url=entry["link"],
    ).serialize()


def extract_data(extraction: models.Extraction) -> Iterable[str]:
    logger.debug(extraction)
    yield from map(convert_data, download_xml_data(build_request_url(extraction)))
