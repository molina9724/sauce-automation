from playwright.sync_api import Locator, Page


class BaseComponent:
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        self.page: Page = page
        self._timeout: int = timeout

    @staticmethod
    def get_parent(locator: Locator) -> Locator:
        return locator.locator("..")
