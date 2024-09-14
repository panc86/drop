import argparse
import logging.config
import time

from worker.config import log_file, log_defaults
from worker.database import get_latest_extractions_to_run, update_executed_extraction
from worker.sources.emm import EMM


logging.config.fileConfig(log_file, defaults=log_defaults)
logger = logging.getLogger("worker")


def foobar(extraction):
    for data_point in EMM(extraction).fetch_data():
        logger.info(data_point)


def run_extractions(extractions):
    if not extractions:
        return
    for extraction in extractions:
        try:
            foobar(extraction)
        except Exception as error:
            logger.error(dict(extraction_id=extraction["id"], error=str(error)))
            continue
        else:
            update_executed_extraction(extraction["id"])


def main():
    parser = argparse.ArgumentParser(
        description="Real time products for Flood Awareness System"
    )
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Run in debug mode."
    )
    args = parser.parse_args()
    logger.setLevel(logging.DEBUG if args.debug else logging.INFO)
    if args.debug:
        foobar(
            {
                "id": "4e5adf30-fefa-4a20-93a0-73512c71c4b6",
                "created_at": "2024-09-13T22:10:00.0000+00:00",
                "executed": True,
                "tag": "probe-extraction",
                "keywords": "probe,test",
                "begin": "2024-09-13T22:10:14.490000+00:00",
                "end": "2024-09-13T22:40:14.490000+00:00",
            }
        )
        return
    while True:
        time.sleep(30)
        run_extractions(get_latest_extractions_to_run())


if __name__ == "__main__":
    main()
