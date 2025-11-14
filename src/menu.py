"""
Menu UI and App logic
"""

import os
import logging
from datetime import datetime

from InquirerPy.base.control import Choice
from InquirerPy.prompts.confirm import ConfirmPrompt
from InquirerPy.prompts.input import InputPrompt
from InquirerPy.prompts.list import ListPrompt
from rich.console import Console
from rich.table import Table

from src.browser_manager import BrowserManager
from src.browser_utils import launch_chrome
from src.constants import APP_VERSION, CHROME_DIR, OUTPUT_DIR
from src.date_utils import count_days, generate_date_range, validate_date
from src.downloader import download


log = logging.getLogger(__name__)
console = Console()


def menu_download():
    today_date = datetime.now().strftime("%Y-%m-%d")
    long_instruction = """Instructions:
- Date format: YYYY-MM-DD
- Future date is invalid
- End date should not be earlier than start date"""

    start_date = InputPrompt(
        message="Enter start date: ",
        default=today_date,
        long_instruction=long_instruction,
        validate=validate_date,
        invalid_message="Invalid input! Read instructions below",
    ).execute()

    end_date = InputPrompt(
        message="Enter end date: ",
        default=today_date,
        long_instruction=long_instruction,
        validate=validate_date,
        invalid_message="Invalid input! Read instructions below",
    ).execute()

    total_days = count_days(start_date, end_date)

    # Check prompt
    table = Table(title=None, show_header=False, box=None)
    table.add_row("Start date", ":", start_date)
    table.add_row("End date", ":", end_date)
    table.add_row("Total work day(s)", ":", total_days)

    console.print()
    console.print(table)
    console.print()

    # Confirmation
    if ConfirmPrompt(message="Start the download process?", default=True).execute():
        dates = generate_date_range(start_date, end_date)
        os.makedirs(OUTPUT_DIR, exist_ok=True)

        with BrowserManager() as bm:
            download(bm, OUTPUT_DIR, dates)


def show_header() -> None:
    """Display header."""
    title = "[bold yellow]IDX Daily 📈[/]"
    subtitle = f"[grey50]{APP_VERSION}[/]"

    console.print(title)
    console.print(subtitle)
    console.print()


def main_menu():
    """Display main menu and return the selected option."""
    console.clear()
    show_header()

    choices = [
        Choice("launch", "🚀 Launch Chrome"),
        Choice("download", "🚩 Start Download"),
        Choice("exit", "👋 Exit"),
    ]

    return ListPrompt(message="Main menu:", choices=choices).execute()


def handle_selection(choice: str):
    """Handle what happens after a selection."""
    match choice:
        case "launch":
            user_data_dir = r"C:\chrome-dev"
            launch_chrome(chrome_path=CHROME_DIR, user_data_dir=user_data_dir)

        case "download":
            menu_download()

        case "exit":
            console.print("\n[bold red]Exiting application...[/]")
            return False

    return True


def run_menu():
    """Menu runner."""
    while True:
        try:
            choice = main_menu()
            if not handle_selection(choice):
                break

        except KeyboardInterrupt:
            console.print("\n[bold red]Operation cancelled by user (Ctrl+C).[/]")
            console.input("Press [bold yellow]ENTER[/] to continue...\n")
            break

        except Exception as e:
            log.error("Error occurred: %s", e)
            console.input("\nPress [bold yellow]ENTER[/] to continue...\n")
            break
