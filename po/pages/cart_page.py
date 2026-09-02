from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.cart_page_item import CartItem
from ..components.left_menu import Menu
# fmt: off
from .base_page import BasePage
# fmt: on
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.item: CartItem = CartItem(page)

        self.continue_shopping_button: Locator = self.page.get_by_role(
            "button", name="Continue Shopping"
        )
        self.checkout_button: Locator = self.page.get_by_role("button", name="Checkout")
        self.cart: Cart = Cart(self.page)
        self.menu: Menu = Menu(self.page)

    def get_inventory_page(self) -> InventoryPage:
        self.continue_shopping_button.click()
        return InventoryPage(self.page)

    def get_checkout_step_1_page(self) -> "CheckoutStepOnePage":
        self.checkout_button.click()
        from .checkout_step_1_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self.page)
