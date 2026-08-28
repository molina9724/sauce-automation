from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from data.routes import INVENTORY, ROOT

from ..pages.login_page import LoginPage
from .base_component import BaseComponent

if TYPE_CHECKING:
    from ..pages.inventory_page import InventoryPage


class Menu(BaseComponent):

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.hamburger_button: Locator = self.page.get_by_role(
            "button", name="Open Menu"
        )
        self.panel: Locator = self.page.locator(".bm-menu-wrap")
        self.item: Locator = self.panel.locator(".menu-item")
        self.logout_link: Locator = self.panel.get_by_role("link", name="Logout")
        self.all_items_link: Locator = self.panel.get_by_role("link", name="All Items")
        self.close_button: Locator = self.panel.locator(".bm-cross-button")

    def logout(self) -> LoginPage:
        self.hamburger_button.click()
        self.logout_link.click()
        self.page.wait_for_url(ROOT)
        return LoginPage(self.page)

    def all_items(self) -> "InventoryPage":
        self.hamburger_button.click()
        self.all_items_link.click()
        self.page.wait_for_url(INVENTORY)
        from ..pages.inventory_page import InventoryPage

        return InventoryPage(self.page)
