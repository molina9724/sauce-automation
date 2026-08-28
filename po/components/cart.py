from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from .base_component import BaseComponent

if TYPE_CHECKING:
    from ..pages.cart_page import CartPage


class Cart(BaseComponent):

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_button: Locator = self.page.locator(".shopping_cart_link")
        self.counter: Locator = self.cart_button.locator(".shopping_cart_badge")

    def get_cart_page(self) -> "CartPage":
        self.cart_button.click()
        from ..pages.cart_page import CartPage

        return CartPage(self.page)
