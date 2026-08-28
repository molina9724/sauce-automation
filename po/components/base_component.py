from typing import Optional

from playwright.sync_api import Locator, Page


class BaseComponent:
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        self.page: Page = page
        self._timeout: int = timeout

    def _timeout_ms(self, timeout: Optional[int]) -> int:
        """Resolve an optional timeout argument to an int (milliseconds).

        This centralizes the common pattern of using an explicit timeout when
        provided or falling back to the instance default. Use this from component
        object methods instead of repeating the conditional everywhere.
        """
        return timeout if timeout is not None else self._timeout

    @staticmethod
    def get_parent(locator: Locator) -> Locator:
        return locator.locator("..")
