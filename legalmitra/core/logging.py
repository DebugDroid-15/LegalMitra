"""
LegalMitra Structured Logging
"""

import logging
import sys
from typing import Optional


def get_logger(name: str = "legalmitra", level: Optional[int] = None) -> logging.Logger:
    """
    Returns a configured logger instance with structured formatting.
    """
    logger = logging.getLogger(name)
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s:%(funcName)s:%(lineno)d] - %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        logger.setLevel(level or logging.INFO)
    elif level is not None:
        logger.setLevel(level)

    return logger

