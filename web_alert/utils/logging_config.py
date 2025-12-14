"""Logging configuration for Web Alert application."""

import logging
from pathlib import Path


def setup_logging():
    """Configure application logging."""
    # Ensure logs directory exists
    Path("logs").mkdir(exist_ok=True)

    logging.basicConfig(
        level=logging.INFO,
        format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        handlers=[logging.FileHandler("logs/web_alert.log"), logging.StreamHandler()],
    )

    # Suppress verbose comtypes logging (used by pyttsx3 on Windows)
    logging.getLogger("comtypes").setLevel(logging.WARNING)

    return logging.getLogger(__name__)
