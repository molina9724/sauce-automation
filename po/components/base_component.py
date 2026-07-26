from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError


class BaseComponent:
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        self._page: Page = page
        self._timeout: int = timeout

    def _timeout_ms(self, timeout: Optional[int]) -> int:
        """Resolve an optional timeout argument to an int (milliseconds).

        This centralizes the common pattern of using an explicit timeout when
        provided or falling back to the instance default. Use this from component
        object methods instead of repeating the conditional everywhere.
        """
        return timeout if timeout is not None else self._timeout

    def _is_item_displayed(
        self, locator: Locator, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_element(
        self, locator: Locator, label: str, timeout: Optional[int] = None
    ) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(locator, timeout_ms):
            return locator
        raise RuntimeError(
            f"Timed out waiting for {label} to be displayed after {timeout_ms} ms"
        )

    @staticmethod
    def get_parent(locator: Locator) -> Locator:
        return locator.locator("..")
