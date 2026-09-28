from playwright.sync_api import Locator, Page

from data.routes import CHECKOUT_COMPLETE, INVENTORY
from po.components.cart_list_component import CartList
from po.pages.checkout_complete import CheckoutComplete
from po.pages.inventory_page import InventoryPage

from ..components.cart_component import Cart
from ..components.left_menu import Menu
from ..pages.base_page import BasePage


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: CartList = CartList(page, timeout)

        self.summary_info: Locator = self.locator(".summary_info")
        self.payment_information: Locator = self.summary_info.locator(
            '[data-test="payment-info-label"]'
        )
        self.payment_method: Locator = self.summary_info.locator(
            '[data-test="payment-info-value"]'
        )

        self.shipping_information: Locator = self.summary_info.locator(
            '[data-test="shipping-info-label"]'
        )
        self.shipping_method: Locator = self.summary_info.locator(
            '[data-test="shipping-info-value"]'
        )

        self.price_total_label: Locator = self.summary_info.locator(
            '[data-test="total-info-label"]'
        )
        self.subtotal: Locator = self.summary_info.locator(".summary_subtotal_label")
        self.tax: Locator = self.summary_info.locator(".summary_tax_label")
        self.total: Locator = self.summary_info.locator(".summary_total_label")

        self.cancel_button: Locator = self.page.get_by_role("button", name="Cancel")
        self.finish_button: Locator = self.page.get_by_role("button", name="Finish")

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
