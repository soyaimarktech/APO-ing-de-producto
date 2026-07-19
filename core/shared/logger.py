"""
Central logging service.

All Core modules must use this logger instead of print().
"""

from __future__ import annotations

import logging


LOGGER_NAME = "apo"


def get_logger() -> logging.Logger:
    """
    Return the shared APO logger.

    Returns:
        Configured logger instance.
    """

    logger = logging.getLogger(LOGGER_NAME)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    handler = logging.StreamHandler()

    formatter = logging.Formatter(
        "[%(levelname)s] %(message)s"
    )

    handler.setFormatter(formatter)

    logger.addHandler(handler)

    return logger
