import logging
import traceback as tb
from playwright.sync_api import sync_playwright


logger = logging.getLogger(__name__)


class Downloader:
    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None
        logger.debug("Downloader initialized")

    def __enter__(self):
        logger.debug("Starting Playwright...")
        self.playwright = sync_playwright().start()
        headless = False
        browser_args = ["--start-maximized"]
        self.browser = self.playwright.chromium.launch(
            headless=headless, args=browser_args
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        logger.info(
            "Browser launched with headless=%s and args=%s", headless, browser_args
        )
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.context:
            logger.debug("Closing context...")
            self.context.close()
        if self.browser:
            logger.debug("Closing browser...")
            self.browser.close()
        if self.playwright:
            logger.debug("Stopping Playwright...")
            self.playwright.stop()
            logger.info("Browser closed")
        if exc_type:
            logger.warning("Exception occurred during session: %s", exc_value)
            logger.debug("Traceback:\n%s", "".join(tb.format_tb(traceback)))
        logger.debug("Downloader session ended")
