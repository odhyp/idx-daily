from playwright.sync_api import sync_playwright


class StockBot:
    URL = "https://idx.co.id/id/data-pasar/ringkasan-perdagangan/ringkasan-saham/"

    def __init__(self):
        self.browser = None
        self.context = None
        self.page = None
        self.playwright = None

    def __enter__(self):
        self.playwright = sync_playwright().start()
        self.browser = self.playwright.chromium.launch(
            headless=False, args=["--start-maximized"]
        )
        self.context = self.browser.new_context(no_viewport=True)
        self.page = self.context.new_page()
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        if self.context:
            self.context.close()
        if self.browser:
            self.browser.close()
        if self.playwright:
            self.playwright.stop()

    def download_file(self, date):
        self.page.goto(self.URL)

        form_date = self.page.locator("input[name='date']")
        form_date.wait_for()
        form_date.click()
        form_date.type(date)
        form_date.press("Enter")

        stock_table = self.page.locator("#vgt-table")
        stock_table.wait_for()

        with self.page.expect_download() as download_info:
            btn_download = self.page.locator('button:has-text("Unduh")')
            btn_download.wait_for()
            btn_download.click()

        download_name = f"stock_{date}"
        download_file = download_info.value
        download_file.save_as(download_name)


def main():
    date = "2024-12-12"

    with StockBot() as bot:
        bot.download_file(date)


if __name__ == "__main__":
    main()
