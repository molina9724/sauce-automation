from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BASE_URL, INVENTORY_URL, BasePage

if TYPE_CHECKING:
    from .login_page import LoginPage


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
        self._inventory_logo: Locator = self.locator(".app_logo")

        self._hamburger_button: Locator = page.get_by_role("button", name="Open Menu")
        self._left_menu: Locator = page.locator(".bm-menu")
        self._logout_link: Locator = page.get_by_role("link", name="Logout")
        self._all_items: Locator = page.locator(".bm-menu-wrap .menu-item")

        self._products_title: Locator = page.locator(".title")
        self._products_filter: Locator = page.get_by_role("combobox")

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        self._hamburger_button.wait_for(state="visible", timeout=timeout_ms)
        return self._hamburger_button

    def open_hamburger_button(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()

    def is_left_menu_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._left_menu.wait_for(state="visible", timeout=timeout_ms)
        return self._left_menu.is_visible()

    def get_left_menu_elements(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_left_menu_displayed(timeout_ms):
            try:
                all_items: List[Locator] = self._all_items.all()
                return [item.inner_text().strip() for item in all_items]
            except PlaywrightTimeoutError:
                raise RuntimeError(
                    f"Timed out waiting for left menu (after {timeout_ms} ms)"
                )
        else:
            raise RuntimeError(f"Left menu was not displayed (after {timeout_ms} ms)")

    def logout(self, timeout: Optional[int] = None) -> "LoginPage":
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self._logout_link.wait_for(state="visible", timeout=timeout_ms)
        self._logout_link.click()
        try:
            self.wait_for_url(BASE_URL, timeout=timeout_ms)
            # local import to avoid circular import
            from .login_page import LoginPage

            return LoginPage(self._page)
        except RuntimeError as e:
            raise RuntimeError(
                f"Timed out waiting for logout to reach {BASE_URL} after {timeout_ms} ms"
            ) from e

    def get_url(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self.wait_for_url(INVENTORY_URL, timeout=timeout_ms)
        return self._page.url

    def get_document_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._inventory_logo.wait_for(state="visible", timeout=timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._inventory_logo.wait_for(state="visible", timeout=timeout_ms)
        return self._inventory_logo.inner_text().strip()

    def get_products_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._products_title.wait_for(state="visible", timeout=timeout_ms)
        return self._products_title.inner_text().strip()

    def is_products_filter_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._products_filter.wait_for(state="visible", timeout=timeout_ms)
        return self._products_filter.is_visible()

    def get_products_filter_object(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_products_filter_displayed(timeout=timeout_ms):
            return self._products_filter
        raise RuntimeError(
            f"Timed out waiting for products filter to be displayed (after {timeout_ms} ms)"
        )

    def get_products_filter_options(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        filter_options: List[Locator] = (
            self.get_products_filter_object(timeout=timeout_ms).locator("option").all()
        )
        all_prices_filter_options: List[str] = [
            filter.inner_text().strip()
            for filter in filter_options
            if filter.inner_text().strip()
        ]
        return all_prices_filter_options

    def get_products_filter_selected_option(self) -> str:
        return self._page.locator(".active_option").inner_text().strip()

    def set_products_filter(self, option: str) -> None:
        self.get_products_filter_object().select_option(option)
