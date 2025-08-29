"""
Logging configuration for the Review Trust System.

Sets up structured logging for monitoring application behaviour and debugging.
"""

import logging
import sys
from pathlib import Path
from typing import Optional


def setup_logging(
    log_level: str = "INFO", log_file: Optional[str] = None
) -> logging.Logger:
    """
    Configure logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR, CRITICAL)
        log_file: Optional file path for log output

    Returns:
        Configured logger instance
    """
    # Create formatter
    formatter = logging.Formatter(
        "%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Configure root logger
    logger = logging.getLogger("review_trust_system")
    logger.setLevel(getattr(logging, log_level.upper()))

    # Console handler
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setFormatter(formatter)
    logger.addHandler(console_handler)

    # File handler (optional)
    if log_file:
        log_path = Path(log_file)
        log_path.parent.mkdir(parents=True, exist_ok=True)

        file_handler = logging.FileHandler(log_file)
        file_handler.setFormatter(formatter)
        logger.addHandler(file_handler)

    return logger


def get_logger(name: str) -> logging.Logger:
    """
    Get a logger instance for a specific module.

    Args:
        name: Name of the module/component

    Returns:
        Logger instance
    """
    return logging.getLogger(f"review_trust_system.{name}")


# Create application logger
app_logger = setup_logging()
