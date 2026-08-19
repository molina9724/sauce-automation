from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_component import BaseComponent

if TYPE_CHECKING:
    from ..pages.cart_page import CartPage

# Selectors
CART_BUTTON: str = ".shopping_cart_link"
CART_COUNTER_BADGE: str = ".shopping_cart_badge"

# Labels
CART_COUNTER: str = "Cart Counter"
CART_BUTTON_LABEL: str = "Cart Button"


class Cart(BaseComponent):

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_button: Locator = self.page.locator(CART_BUTTON)
        self.cart_counter: Locator = self.cart_button.locator(CART_COUNTER_BADGE)

    def get_cart_page(self, timeout: Optional[int] = None) -> "CartPage":
        timeout_ms: int = self._timeout_ms(timeout)
        cart_button: Locator = self.get_element(
            self.cart_button, CART_BUTTON_LABEL, timeout_ms
        )
        cart_button.click()
        from ..pages.cart_page import CartPage

        return CartPage(self.page)

    def get_cart_counter(self, timeout: Optional[int] = None) -> int:
        timeout_ms: int = self._timeout_ms(timeout)
        cart_counter: Locator = self.get_element(
            self.cart_counter, CART_COUNTER, timeout_ms
        )
        counter: str = cart_counter.inner_text().strip()
        try:
            return int(counter)
        except ValueError:
            raise RuntimeError(
                f"{CART_COUNTER} is returning a value that cannot be converted to int"
            )

    def is_cart_empty(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self.cart_counter.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False
