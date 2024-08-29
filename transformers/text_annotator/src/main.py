from core import model
from consumer import consume_events


def main():
    topics = ["raw_texts"]
    consume_events(topics, handler=model.get_annotator())


if __name__ == '__main__':
    main()
