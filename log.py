# coding=utf8


import logging
import os

LOG_FILE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "logs/strack_event.log")


def get_logger():
    logger = logging.getLogger("strack_event")
    logger.setLevel(level=logging.INFO)
    handler = logging.FileHandler(LOG_FILE)
    # handler = logging.handlers.RotatingFileHandler(LOG_FILE, maxBytes=1024 * 1024, backupCount=40)
    handler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    handler.setFormatter(formatter)

    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    logger.addHandler(handler)
    logger.addHandler(console)
    return logger
