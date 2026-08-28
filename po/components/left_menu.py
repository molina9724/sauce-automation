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

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        hamburger_button: Locator = self.get_element(
            self.hamburger_button, HAMBURGER_BUTTON, timeout_ms
        )
        return hamburger_button

    def is_hamburger_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self.hamburger_button, timeout_ms)

    # This button is a sibling of LeftMenu, not a children
    def open(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        hamburger_button: Locator = self.get_element(
            self.hamburger_button, HAMBURGER_BUTTON, timeout_ms
        )
        hamburger_button.click()

    def close(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        close_button: Locator = self.get_element(
            self.close_button, CLOSE_ERROR_BUTTON, timeout_ms
        )
        close_button.click()

    def get_logout(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        logout: Locator = self.get_element(self.logout_link, LOGOUT_LINK, timeout_ms)
        return logout

    def get_all_items(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        all_items: Locator = self.get_element(
            self.all_items_link, ALL_ITEMS, timeout_ms
        )
        return all_items

    def is_left_menu_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self.panel, timeout_ms)

    def is_left_menu_hidden(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_hidden(self.panel, timeout_ms)

    def get_left_menu_elements(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        left_menu: Locator = self.get_element(self.panel, LEFT_MENU, timeout_ms)
        all_items: List[Locator] = left_menu.locator(LEFT_MENU_ITEM).all()
        return [item.inner_text().strip() for item in all_items]

    def logout(self, timeout: Optional[int] = None) -> LoginPage:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self.get_logout(timeout_ms).click()
        try:
            self.wait_for_url(BASE_URL, timeout=timeout_ms)
            return LoginPage(self.page)
        except RuntimeError as exception:
            raise RuntimeError(
                f"Timed out waiting for logout to reach {BASE_URL} after {timeout_ms} ms"
            ) from exception

    def all_items(self) -> "InventoryPage":
        self.hamburger_button.click()
        self.all_items_link.click()
        self.wait_for_url(INVENTORY_URL)
        from ..pages.inventory_page import InventoryPage

        return InventoryPage(self.page)
