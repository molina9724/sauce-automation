from playwright.sync_api import Locator, Page

from data.inventory_data import ADD_TO_CART

from ..components.base_item import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, ".inventory_item", timeout)
        self.image: Locator = self.root.locator("img[class='inventory_item_img']")
        # Add to cart and Remove buttons are the same
        self.button: Locator = self.root.locator(".btn_inventory")

    def add(self, index: int) -> None:
        item: Locator = self.root.nth(index)
        item.get_by_role("button", name=ADD_TO_CART).click()
