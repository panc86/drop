from datetime import datetime
import logging
from typing import Any, Iterable
import urllib.parse

import pandas


logger = logging.getLogger(__name__)


class EMM:
    def __init__(self, extraction: dict[str, str]) -> None:
        self.extraction = extraction

    def build_request_url(self) -> str:
        date_format = "%Y-%m-%dT%H:%M:%SZ"
        url = "https://emm.newsbrief.eu/rss/rss?{params}"
        return url.format(
            params=urllib.parse.urlencode(
                dict(
                    language="all",
                    type="search",
                    mode="advanced",
                    datefrom=datetime.fromisoformat(self.extraction["begin"]).strftime(date_format),
                    dateto=datetime.fromisoformat(self.extraction["end"]).strftime(date_format),
                    atLeast=self.extraction["keywords"].replace(",", "+"),
                    duplicates="false",
                )
            )
        )

    def download_data(self) -> Iterable[dict[str, Any]]:
        try:
            yield from pandas.read_xml(self.build_request_url(), parser="etree", xpath=".//item").to_dict(orient="records")
        except ValueError as error:
            logger.error(dict(url=self.build_request_url(), error=error))
            return []

    def fetch_data(self) -> Iterable[dict[str, Any]]:
        for data_point in self.download_data():
            yield dict(
                extraction_id=self.extraction["id"],
                created_at=datetime.strptime(data_point["pubDate"], "%a, %d %b %Y %H:%M:%S %z"),
                id=data_point["guid"],
                lang=data_point["language"],
                text=data_point["title"],
                url=data_point["link"],
                source="emm"
            )
