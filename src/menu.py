"""
Menu UI and App logic
"""

import logging
from datetime import datetime

from InquirerPy.prompts.confirm import ConfirmPrompt
from InquirerPy.separator import Separator
from rich.console import Console


log = logging.getLogger(__name__)
console = Console()

def show_header() -> None:
    """Display header."""
    title = "[bold yellow]IDX Daily 📈[/]"
    subtitle = f"[grey50]{APP_VERSION}[/]"

    console.print(title)
    console.print(subtitle)
    console.print()


def main_menu():
    """Display main menu and return the selected option."""
    pass


def handle_selection(choice: str):
    """Handle what happens after a selection."""
    pass


def run_menu():
    """Menu runner."""
    pass
