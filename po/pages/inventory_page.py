from playwright.sync_api import Locator, Page

from .base_page import BasePage

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
