"""
Browser Manager
Handles Playwright connection to an existing Chrome session via CDP.
"""

import logging
from typing import Optional
from types import TracebackType

from playwright.sync_api import (
    sync_playwright,
    Playwright,
    Browser,
    BrowserContext,
    Page,
    Error,
)


log = logging.getLogger(__name__)


class BrowserManager:
    """Manage Playwright connection via CDP."""

    def __init__(self, cdp_url: str = "http://localhost:9222") -> None:
        self.cdp_url = cdp_url
        self.playwright: Optional[Playwright] = None
        self.browser: Optional[Browser] = None
        self.context: Optional[BrowserContext] = None
        self.page: Optional[Page] = None

    def __enter__(self) -> "BrowserManager":
        """Connect to existing browser via CDP."""
        log.info("Connecting to Chrome via CDP...")

        try:
            self.playwright = sync_playwright().start()
            self.browser = self.playwright.chromium.connect_over_cdp(self.cdp_url)
            self.context = self.browser.contexts[0]
            self.page = self.context.pages[0]
            log.info("✅ Chrome connected successfully")
            return self

        except Error as e:
            log.error("❌ Failed to connect to Chrome via CDP: %s", e)
            raise ConnectionError(
                "Could not connect to Chrome. Is it running with --remote-debugging-port=9222?"
            ) from e

        except Exception as e:
            log.error("Unexpected error during CDP connection: %s", e)
            raise

    def __exit__(
        self,
        exc_type: Optional[type[BaseException]],
        exc_value: Optional[BaseException],
        traceback: Optional[TracebackType],
    ) -> None:
        """Clean up resources and log exceptions if any."""
        if exc_type:
            log.error("❌ Exception in BrowserManager", exc_info=True)

        try:
            if self.browser:
                # Cannot close the default context from CDP
                log.debug("Closing browser connection...")
                self.browser.close()

        except Exception as e:
            log.warning("⚠️ Failed to close browser: %s", e)

        finally:
            if self.playwright:
                self.playwright.stop()
                log.debug("Playwright stopped cleanly")

    @property
    def page_safe(self) -> Page:
        """Return the Playwright Page, ensuring it's initialized."""
        if self.page is None:
            raise RuntimeError(
                "Page not initialized. Use inside a 'with BrowserManager():' block."
            )
        return self.page
