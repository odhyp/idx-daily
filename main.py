import datetime
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

    def download_file(self, dates: list):
        self.page.goto(self.URL)

        for date in dates:
            # Date form
            form_date = self.page.locator("input[name='date']")
            form_date.wait_for()
            form_date.click()
            form_date.clear()
            form_date.type(date)
            form_date.press("Enter")

            # Table
            stock_table = self.page.locator("#vgt-table")
            stock_table.wait_for()

            # Download button
            btn_download = self.page.locator('button:has-text("Unduh")')

            if btn_download.is_enabled():
                with self.page.expect_download() as download_info:
                    btn_download.wait_for()
                    btn_download.click()

                download_name = f"stock_{date}.xlsx"
                download_file = download_info.value
                download_file.save_as(download_name)

            elif btn_download.is_disabled():
                continue

            else:
                continue


def generate_date_range(start_date: str, end_date: str) -> list:
    formatted_start_date = datetime.datetime.strptime(start_date, "%Y-%m-%d")
    formatted_end_date = datetime.datetime.strptime(end_date, "%Y-%m-%d")

    date_range_length = (formatted_end_date - formatted_start_date).days + 1

    date_list = [
        (formatted_start_date + datetime.timedelta(days=i)).strftime("%Y-%m-%d")
        for i in range(date_range_length)
    ]

    return date_list


def main():
    start_date = "2024-01-01"
    end_date = "2024-01-05"

    dates = generate_date_range(start_date, end_date)

    with StockBot() as bot:
        bot.download_file(dates)


if __name__ == "__main__":
    main()
