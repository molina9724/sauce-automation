from playwright.sync_api import Locator, Page

from ..components.base_component import BaseComponent


class BaseItem(BaseComponent):
    def __init__(self, page: Page, item_selector: str, timeout: int) -> None:
        super().__init__(page, timeout)
        self.root: Locator = self.page.locator(item_selector)
        self.name: Locator = self.root.locator(".inventory_item_name")
        self.price: Locator = self.root.locator(".inventory_item_price")
        self.description: Locator = self.root.locator(".inventory_item_desc")

    def remove(self, index: int) -> None:
        item: Locator = self.root.nth(index)
        item.get_by_role("button", name="Remove").click()
