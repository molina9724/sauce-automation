# fmt: off
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from data.cart_data import YOUR_CART
from po.components.cart_list_component import CartList

from ..components.cart_component import Cart
from ..components.left_menu import Menu
from .base_page import BasePage
from .inventory_page import InventoryPage

# fmt: on

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.title: Locator = self.page.get_by_text(YOUR_CART)

        self.continue_shopping_button: Locator = self.page.get_by_role(
            "button", name="Continue Shopping"
        )
        self.checkout_button: Locator = self.page.get_by_role("button", name="Checkout")
        self.cart: Cart = Cart(self.page)
        self.menu: Menu = Menu(self.page)
        self.cart_list: CartList = CartList(page, timeout)

    def get_inventory_page(self) -> InventoryPage:
        self.continue_shopping_button.click()
        return InventoryPage(self.page)

    def get_checkout_step_1_page(self) -> "CheckoutStepOnePage":
        self.checkout_button.click()
        from .checkout_step_1_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self.page)
