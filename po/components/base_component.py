from typing import Union

from playwright.sync_api import Locator, Page


class BaseComponent:
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        self.page: Page = page
        self._timeout: int = timeout

    @staticmethod
    def get_parent(locator: Locator) -> Locator:
        return locator.locator("..")

    def locator(self, selector_or_locator: Union[str, Locator]) -> Locator:
        """
        Returns a Playwright Locator object for the given selector or locator.

        Args:
            selector_or_locator (Union[str, Locator]): A CSS selector string or an existing Locator object.

        Returns:
            Locator: A Playwright Locator object corresponding to the selector or the provided Locator.
        """
        if isinstance(selector_or_locator, str):
            return self.page.locator(selector_or_locator)
        else:
            return selector_or_locator
