from playwright.sync_api import Page

from .base_page import BasePage


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
