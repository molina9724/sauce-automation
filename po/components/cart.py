from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

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
        self.counter: Locator = self.cart_button.locator(CART_COUNTER_BADGE)

    def get_cart_page(self) -> "CartPage":
        self.cart_button.click()
        from ..pages.cart_page import CartPage

        return CartPage(self.page)
