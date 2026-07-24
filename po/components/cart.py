from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from ..pages.base_page import CART_URL, BasePage

if TYPE_CHECKING:
    _Base = BasePage
    from sauce_project.po.pages.cart_page import CartPage
else:
    _Base = object

# Selectors
CART_BUTTON: str = ".shopping_cart_link"
CART_COUNTER_BADGE: str = ".shopping_cart_badge"

# Labels
CART_COUNTER: str = "Cart Counter"


class Cart(_Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._cart_button: Locator = self._page.locator(CART_BUTTON)
        self._cart_counter: Locator = self._cart_button.locator(CART_COUNTER_BADGE)

    def get_cart_page(self, timeout: Optional[int] = None) -> "CartPage":
        timeout_ms: int = self._timeout_ms(timeout)
        cart_button: Locator = self.get_element(self._cart_button, CART_URL, timeout_ms)
        cart_button.click()
        from sauce_project.po.pages.cart_page import CartPage

        return CartPage(self._page)

    def get_cart_counter(self, timeout: Optional[int] = None) -> int:
        timeout_ms: int = self._timeout_ms(timeout)
        cart_counter: Locator = self.get_element(
            self._cart_counter, CART_COUNTER, timeout_ms
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
            self._cart_counter.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False
