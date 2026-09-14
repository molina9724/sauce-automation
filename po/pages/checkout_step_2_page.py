from playwright.sync_api import Locator, Page

from data.routes import CHECKOUT_COMPLETE, INVENTORY
from po.components.cart_page_item import CartItem
from po.pages.checkout_complete import CheckoutComplete
from po.pages.inventory_page import InventoryPage

from ..components.cart import Cart
from ..components.left_menu import Menu
from ..pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.subtotal: Locator = self.locator(".summary_subtotal_label")
        self.tax: Locator = self.locator(".summary_tax_label")
        self.total: Locator = self.locator(".summary_total_label")

        self.cancel_button: Locator = self.page.get_by_role("button", name="Cancel")
        self.finish_button: Locator = self.page.get_by_role("button", name="Finish")

        self.item: CartItem = CartItem(page)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)

    def cancel(self) -> InventoryPage:
        self.cancel_button.click()
        self.page.wait_for_url(INVENTORY)
        return InventoryPage(self.page)

    def finish(self) -> CheckoutComplete:
        self.finish_button.click()
        self.page.wait_for_url(CHECKOUT_COMPLETE)
        return CheckoutComplete(self.page)
