from argparse import ArgumentParser
import logging.config
import os
import warnings

from app import geocoder, broker


# ignore warnings
warnings.filterwarnings("ignore")


file_dir = os.path.dirname(__file__)
os.makedirs(os.path.join(file_dir, "log"), exist_ok=True)
log_file = os.path.join(file_dir, "logging.ini")
log_defaults = {'logfilename': os.path.join(file_dir, "log", "errors.log")}
logging.config.fileConfig(log_file, defaults=log_defaults)

    
def main():
    parser = ArgumentParser(description="Geocode events in batches.")
    parser.add_argument(
        "--debug", action="store_true", default=False, help="Run in debug mode."
    )
    parser.add_argument(
        "--listen", action="store_true", default=False, help="Run as listener."
    )
    parser.add_argument(
        "--worker", action="store_true", default=False, help="Run as job worker."
    )
    args = parser.parse_args()
    logger = logging.getLogger("app")
    if args.debug:
        logger.setLevel(logging.DEBUG)
    if args.listen:
        model = geocoder.get_model()
        for batch in broker.consume_batched_events():
            broker.log_events(model(batch))
            #job = jobs.enqueue_job(extraction)
            #logger.info(dict(job=dict(id=job.id, status=job.get_status()), extraction=extraction))
    if args.worker:
        pass
        #jobs.worker.work()


if __name__ == "__main__":
    main()
