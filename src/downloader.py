"""
Execute download session
"""

import logging

from src.browser_manager import BrowserManager
from src.constants import BASE_URL


log = logging.getLogger(__name__)


def download(bm: BrowserManager, output_dir: str, dates: list) -> None:
    """Download Ringkasan Saham using BrowserManager."""
    log.info("🚩 Starting download...")

    # Initialize
    page = bm.page_safe
    page.goto(BASE_URL)

    for date in dates:
        # Date form
        form_date = page.locator("input[name='date']")
        form_date.wait_for()
        form_date.click()
        form_date.clear()
        form_date.type(date)
        form_date.press("Enter")

        # Table
        stock_table = page.locator("#vgt-table")
        stock_table.wait_for()

        # Download button
        btn_download = page.locator("button", has_text="Unduh")

        if btn_download.is_enabled():
            with page.expect_download() as download_info:
                btn_download.wait_for()
                btn_download.click()

            download_name = f"{date}.xlsx"
            download_path = f"{output_dir}/{download_name}"
            download_file = download_info.value
            download_file.save_as(download_path)
            log.info("Download success: %s", download_name)

        elif btn_download.is_disabled():
            continue

        else:
            continue
