from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator

from sauce_project.po.pages.base_page import BASE_URL, BasePage
from sauce_project.po.pages.login_page import LoginPage

if TYPE_CHECKING:
    _Base = BasePage
else:
    _Base = object

# Selectors
LEFT_MENU_ITEM: str = ".menu-item"

# Textbox names
LOGOUT: str = "Logout"

# Labels
HAMBURGER_BUTTON: str = "Hamburger Button"
LEFT_MENU: str = "Left Menu"
LOGOUT_LINK: str = "Logout Link"


class LeftMenu(_Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._hamburger_button: Locator = self._page.get_by_role(
            "button", name="Open Menu"
        )
        self._left_menu: Locator = self._page.locator(".bm-menu")
        self._left_menu_item: Locator = self._left_menu.locator(LEFT_MENU_ITEM)
        self._logout_link: Locator = self._left_menu.get_by_role("link", name=LOGOUT)

    def get_hamburger_button(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        hamburger_button: Locator = self.get_element(
            self._hamburger_button, HAMBURGER_BUTTON, timeout_ms
        )
        return hamburger_button

    def open_hamburger_button(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()

    def get_logout_link(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        logout: Locator = self.get_element(self._logout_link, LOGOUT_LINK, timeout_ms)
        return logout

    def is_left_menu_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._left_menu, timeout_ms)

    def get_left_menu_elements(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        left_menu: Locator = self.get_element(self._left_menu, LEFT_MENU, timeout_ms)
        all_items: List[Locator] = left_menu.locator(LEFT_MENU_ITEM).all()
        return [item.inner_text().strip() for item in all_items]

    def logout(self, timeout: Optional[int] = None) -> LoginPage:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_hamburger_button(timeout_ms).click()
        self.get_logout_link(timeout_ms).click()
        try:
            self.wait_for_url(BASE_URL, timeout=timeout_ms)
            return LoginPage(self._page)
        except RuntimeError as exception:
            raise RuntimeError(
                f"Timed out waiting for logout to reach {BASE_URL} after {timeout_ms} ms"
            ) from exception
