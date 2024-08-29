import logging.config
import os

from extract import extractor
from extract.api import router
from extract.db.core import engine
from extract.db.models import Base

# initialize database
Base.metadata.create_all(bind=engine)


if __name__ == "__main__":
    logging.config.fileConfig(os.path.join(os.path.dirname(__file__), "logging.ini"))
    extractor.run()
