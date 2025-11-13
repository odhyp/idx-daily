"""
Logging setup
"""

import logging
from datetime import datetime
from pathlib import Path


def setup_logging() -> None:
    """Configure Rich + File logging and return a logger."""
    log_dir = Path("logs")
    log_dir.mkdir(exist_ok=True)
    log_filename = datetime.now().strftime("%Y-%m-%d") + ".log"
    log_path = log_dir / log_filename

    # File handler (include DEBUG, for log file)
    file_handler = logging.FileHandler(log_path, encoding="utf-8")
    file_handler.setLevel(logging.DEBUG)
    file_handler.setFormatter(
        logging.Formatter(
            fmt="%(asctime)s [%(levelname)s] [%(name)s] %(message)s",
            datefmt="%Y-%m-%d %H:%M:%S",
        )
    )

    # Root logger setup
    root_logger = logging.getLogger()
    root_logger.setLevel(logging.DEBUG)
    root_logger.addHandler(file_handler)
