import logging
import os
from logging.handlers import RotatingFileHandler

def setup_logging():
    os.makedirs("logs", exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)-30s | %(message)s"
    )

    # File log
    file_handler = RotatingFileHandler(
        "logs/rover.log",
        maxBytes=5_000_000,
        backupCount=3
    )
    file_handler.setFormatter(formatter)

    # Console log
    console_handler = logging.StreamHandler()
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)