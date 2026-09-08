from playwright.sync_api import Locator, Page

from data.routes import INVENTORY
from po.pages.base_page import BasePage
from po.pages.inventory_page import InventoryPage


class CheckoutComplete(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.title: Locator = self.page.locator(".title")

        self.checkout_container: Locator = self.locator("#checkout_complete_container")
        self.heavy_check_mark: Locator = self.checkout_container.locator(
            "img.pony_express"
        )
        self.header: Locator = self.checkout_container.get_by_role(
            "heading", name="Thank you for your order!"
        )
        self.text: Locator = self.checkout_container.locator(".complete-text")

        self.back_button: Locator = self.page.get_by_role("button", name="Back Home")

    def get_inventory_page(self) -> InventoryPage:
        self.back_button.click()
        self.page.wait_for_url(INVENTORY)
        return InventoryPage(self.page)
