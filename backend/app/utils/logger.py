import logging
from pathlib import Path

from app.config import LOG_FOLDER

log_directory = Path(LOG_FOLDER)

log_directory.mkdir(parents=True, exist_ok=True)

logger = logging.getLogger("TranscriBITE")
logger.setLevel(logging.INFO)

file_handler = logging.FileHandler(
    log_directory / "application.log",
    encoding="utf-8"
)

formatter = logging.Formatter(
    "%(asctime)s | %(levelname)s | %(message)s"
)

file_handler.setFormatter(formatter)

if not logger.handlers:
    logger.addHandler(file_handler)
