from logging import getLogger, StreamHandler, DEBUG, INFO, Formatter
from sys import stdout


def set_logger():
    logger = getLogger(__name__)
    logger.setLevel(INFO)
    ch = StreamHandler(stdout)
    ch.setLevel(DEBUG)
    formatter = Formatter('%(asctime)s - %(levelname)s - %(message)s')
    ch.setFormatter(formatter)
    logger.addHandler(ch)
    return logger

