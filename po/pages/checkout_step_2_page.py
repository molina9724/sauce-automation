from decimal import Decimal

from playwright.sync_api import Locator, Page

from po.components.cart_page_item import CartItem

from ..components.cart import Cart
from ..components.left_menu import Menu
from ..pages.base_page import BasePage

TAXES: Decimal = Decimal("0.08")
CURRENCY = "$"


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.subtotal: Locator = self.locator(".summary_subtotal_label")
        self.tax: Locator = self.locator(".summary_tax_label")
        self.total: Locator = self.locator(".summary_total_label")

        self.item: CartItem = CartItem(page)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)
