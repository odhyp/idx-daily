"""
IDX Daily

Author: Odhy Pradhana
License: MIT License
Year: 2025
"""

import logging

from src.logging_setup import setup_logging
from src.menu import run_menu

setup_logging()
log = logging.getLogger(__name__)


def run():
    """Run the app."""
    log.debug("Starting IDX Daily...")
    run_menu()
    log.debug("Goodbye!")


if __name__ == "__main__":
    run()
