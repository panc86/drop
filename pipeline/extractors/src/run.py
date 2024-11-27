from argparse import ArgumentParser
import logging

from app import broker, events


# setup logging
console_handler = logging.StreamHandler()
console_handler.setLevel(logging.DEBUG)
file_handler = logging.FileHandler("/tmp/extractors.log")
file_handler.setLevel(logging.ERROR)


def main():
    parser = ArgumentParser(description="Extract events from data sources.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Run in debug mode."
    )
    parser.add_argument(
        "--topic",
        default="events",
        help="Kafka topic to send events. Default is %(default)s topic.",
    )
    args = parser.parse_args()
    logging.basicConfig(
        handlers=[console_handler, file_handler],
        level=logging.DEBUG if args.debug else logging.INFO)

    for extraction in broker.listen_for_incoming_extractions():
        broker.log_events(events.fetch_events(extraction), topic=args.topic)


if __name__ == "__main__":
    main()
