from playwright.sync_api import Locator, Page

from po.components.base_component import BaseComponent


class InventoryItemDetails(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.root: Locator = self.locator("#inventory_item_container")
        self.name: Locator = self.root.locator(".inventory_details_name")
        self.price: Locator = self.root.locator(".inventory_details_price")
        self.description: Locator = self.root.locator(".inventory_details_desc")
        self.button: Locator = self.root.get_by_role("button")
        self.image: Locator = self.root.get_by_role("img")
