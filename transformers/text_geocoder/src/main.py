import warnings

from consumer import consume_events
from core import model

# ignore warnings
warnings.filterwarnings("ignore")


def main():
    topics = ["annotated_texts"]
    consume_events(topics, handler=model.get_geocoder())


if __name__ == '__main__':
    main()
