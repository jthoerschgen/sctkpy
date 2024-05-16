import datetime
import logging
import os

from .config import logs_dir

# Set up logging for project
logging_format = "%(asctime)s %(levelname)-8s %(message)s"

logging.basicConfig(
    format=logging_format,
    level=logging.DEBUG,
    datefmt="%Y-%m-%d %H:%M:%S",
    filename=os.path.join(
        logs_dir,
        f"{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}.log",
    ),
)

logger = logging.getLogger(__name__)
