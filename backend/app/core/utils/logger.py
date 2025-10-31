import logging
import sys
from logging.handlers import RotatingFileHandler
from pathlib import Path

# Optional: create a logs directory
LOG_DIR = Path(__file__).resolve().parent.parent / "logs"
LOG_DIR.mkdir(exist_ok=True)

LOG_FILE = LOG_DIR / "app.log"


def get_logger(name: str = "app") -> logging.Logger:
    """Return a configured logger instance (singleton per name)."""
    logger = logging.getLogger(name)

    # Avoid reconfiguring if already initialized
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # --- Formatter ---
    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-8s | %(name)s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # --- Console Handler ---
    console_handler = logging.StreamHandler(sys.stdout)
    console_handler.setLevel(logging.INFO)
    console_handler.setFormatter(formatter)

    # --- Rotating File Handler ---
    file_handler = RotatingFileHandler(
        LOG_FILE, maxBytes=5 * 1024 * 1024, backupCount=5, encoding="utf-8"
    )
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(formatter)

    # --- Attach Handlers ---
    logger.addHandler(console_handler)
    logger.addHandler(file_handler)

    logger.propagate = False  # Prevent double logging in uvicorn
    return logger


# Global default logger instance
logger = get_logger("app")
