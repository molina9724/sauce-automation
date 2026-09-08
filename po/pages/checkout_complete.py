from playwright.sync_api import Locator, Page

from po.pages.base_page import BasePage


class CheckoutComplete(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.title: Locator = self.page.locator(".title")
