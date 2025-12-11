"""Structured logging configuration.

Provides consistent logging format and level management across the application.
"""

import logging
import os
from logging.handlers import RotatingFileHandler

# Get log level from environment or default to INFO
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO").upper()


def setup_logging(name: str) -> logging.Logger:
    """Configure and return a logger instance.

    Args:
        name: Logger name (usually __name__)

    Returns:
        logging.Logger: Configured logger instance
    """
    logger = logging.getLogger(name)

    # Only configure if not already configured
    if logger.handlers:
        return logger

    logger.setLevel(getattr(logging, LOG_LEVEL))

    # Console handler with formatting
    console_handler = logging.StreamHandler()
    console_handler.setLevel(getattr(logging, LOG_LEVEL))

    # Formatter
    formatter = logging.Formatter(
        fmt="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )
    console_handler.setFormatter(formatter)

    # Add handler to logger
    logger.addHandler(console_handler)

    # Optional: File handler for production
    if os.getenv("LOG_FILE"):
        file_handler = RotatingFileHandler(
            os.getenv("LOG_FILE"),
            maxBytes=10485760,  # 10MB
            backupCount=5,
        )
        file_handler.setLevel(getattr(logging, LOG_LEVEL))
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


# Global logger instance
logger = setup_logging("app")
