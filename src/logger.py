import logging
from functools import cache

from src.settings import Settings

LOG_FORMAT_DEBUG = '%(levelname)s:     %(message)s : %(funcName)s'

@cache
def configure_logging() -> None:
    """Configure logging."""
    settings = Settings.load()
    logging.basicConfig(level=settings.LOG_LEVEL, format=LOG_FORMAT_DEBUG)
