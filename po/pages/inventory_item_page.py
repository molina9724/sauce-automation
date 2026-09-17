from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from data.routes import INVENTORY
from po.components.left_menu import Menu
from po.pages.base_page import BasePage

from ..components.cart_component import Cart
from ..components.inventory_item import InventoryItem

if TYPE_CHECKING:
    from .inventory_page import InventoryPage


class InventoryItemPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.back_to_products_button: Locator = self.page.get_by_role(
            "button", name="Back to products"
        )

        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)
        self.item: InventoryItem = InventoryItem(page)

    def back_to_products(self) -> "InventoryPage":
        self.back_to_products_button.click()
        self.page.wait_for_url(INVENTORY)
        from .inventory_page import InventoryPage

        return InventoryPage(self.page)
