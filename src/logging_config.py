from pathlib import Path
import logging
from logging.handlers import RotatingFileHandler

def setup_logging(log_file="logs/rover.log", console_level=logging.INFO):
    log_path = Path(log_file)
    log_path.parent.mkdir(parents=True, exist_ok=True)

    logger = logging.getLogger()
    logger.setLevel(logging.DEBUG)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)-7s | %(name)-25s | %(message)s"
    )

    if logger.handlers:
        return logger

    file_handler = RotatingFileHandler(
        log_path,
        maxBytes=5_000_000,
        backupCount=3,
        encoding="utf-8"
    )

    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(console_level)
    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)

    return logger