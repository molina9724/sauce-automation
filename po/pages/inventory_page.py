from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BASE_URL, BasePage

INVENTORY_URL = "https://www.saucedemo.com/inventory.html"


class InventoryPage(BasePage):
    """
    Page object model for the inventory page.

    Inherits from BasePage and provides functionality specific to the inventory page,
    such as accessing the inventory container element.

    Attributes:
        _inventory_container (Locator): Locator for the inventory container element.

    Args:
        page (Page): The Playwright Page object to interact with.
        timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
    """

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        """
        Initializes the InventoryPage with a Playwright Page instance and an optional timeout.

        Sets up the locator for the inventory container element.

        Args:
            page (Page): The Playwright Page object to interact with.
            timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
        """
        super().__init__(page, timeout)
        self._inventory_container: Locator = self.locator("#inventory_container")

        self._hamburger_button: Locator = page.get_by_role("button", name="Open Menu")
        self._logout_link: Locator = page.get_by_role("link", name="Logout")

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms = self._timeout_ms(timeout)
        self._hamburger_button.wait_for(state="visible", timeout=timeout_ms)
        return self._hamburger_button

    def logout(self, timeout: Optional[int] = None):
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self._logout_link.wait_for(state="visible", timeout=timeout_ms)
        self._logout_link.click()
        try:
            self.wait_for_url(BASE_URL, timeout=timeout_ms)
            from .login_page import LoginPage

            return LoginPage(self._page)
        except PlaywrightTimeoutError as e:
            raise RuntimeError(
                f"Timed out waiting for logout to reach {BASE_URL} after {timeout_ms} ms"
            ) from e
