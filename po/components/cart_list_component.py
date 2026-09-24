from playwright.sync_api import Locator, Page

from data.cart_data import DESCRIPTION, QUANTITY
from po.components.base_component import BaseComponent
from po.components.cart_item import CartItem


class CartList(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.root: Locator = self.locator(".cart_list")
        self.quantity: Locator = self.root.get_by_text(QUANTITY)
        self.description: Locator = self.root.get_by_text(DESCRIPTION)
        self.item: CartItem = CartItem(page, timeout)
