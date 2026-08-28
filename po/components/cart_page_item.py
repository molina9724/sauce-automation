from playwright.sync_api import Locator, Page

from ..components.base_item import BaseItem


class CartItem(BaseItem):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, ".cart_item", timeout)
        self.quantity: Locator = self.root.locator(".cart_quantity")
