from playwright.sync_api import Locator

from ..components.base_item import BaseItem


class InventoryItem(BaseItem):
    def __init__(self, page, timeout=10000) -> None:
        super().__init__(page, ".inventory_item", timeout)
        self.image: Locator = self.root.locator("img[class='inventory_item_img']")
