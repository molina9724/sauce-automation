from playwright.sync_api import Locator

from ..components.base_component import BaseComponent


class BaseItem(BaseComponent):
    def __init__(self, page, item_selector: str, timeout) -> None:
        super().__init__(page, timeout)
        self.root: Locator = self.page.locator(item_selector)
        self.name: Locator = self.root.locator(".inventory_item_name")
        self.price: Locator = self.root.locator(".inventory_item_price")
        self.description: Locator = self.root.locator(".inventory_item_desc")
        self.remove_button: Locator = self.root.get_by_role("button", name="Remove")
