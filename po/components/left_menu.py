from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page

from ..pages.base_page import BASE_URL, INVENTORY_URL
from ..pages.login_page import LoginPage
from .base_component import BaseComponent

if TYPE_CHECKING:
    from ..pages.inventory_page import InventoryPage
else:
    _Base = object

# Selectors
LEFT_MENU_ITEM: str = ".menu-item"

# Textbox names
LOGOUT: str = "Logout"

# Labels
HAMBURGER_BUTTON: str = "Hamburger Button"
CLOSE_ERROR_BUTTON: str = "Close error button"
LEFT_MENU: str = "Left Menu"
LOGOUT_LINK: str = "Logout Link"
ALL_ITEMS: str = "All Items"


class Menu(BaseComponent):

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.hamburger_button: Locator = self.page.get_by_role(
            "button", name="Open Menu"
        )
        self.panel: Locator = self.page.locator(".bm-menu-wrap")
        self.item: Locator = self.panel.locator(LEFT_MENU_ITEM)
        self.logout_link: Locator = self.panel.get_by_role("link", name=LOGOUT)
        self.all_items_link: Locator = self.panel.get_by_role("link", name=ALL_ITEMS)
        self.close_button: Locator = self.panel.locator(".bm-cross-button")

    def logout(self) -> LoginPage:
        self.hamburger_button.click()
        self.logout_link.click()
        self.wait_for_url(BASE_URL)
        return LoginPage(self.page)

    def all_items(self) -> "InventoryPage":
        self.hamburger_button.click()
        self.all_items_link.click()
        self.wait_for_url(INVENTORY_URL)
        from ..pages.inventory_page import InventoryPage

        return InventoryPage(self.page)
