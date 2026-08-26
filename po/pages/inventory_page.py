from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.inventory_page_item import InventoryItem
from ..components.left_menu import Menu
from .base_page import BasePage


class InventoryPage(BasePage):
    """
    Page object model for the inventory page.

    Inherits from BasePage and provides functionality specific to the inventory page,
    such as accessing the inventory container element.

    Attributes:

    Args:
        page (Page): The Playwright Page object to interact with.
        timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
    """

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        """
        Initializes the InventoryPage with a Playwright Page instance and an optional timeout.

        Sets up the locator for the inventory container element.

        Args:
            page (Page): The Playwright Page object to interact with.
            timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
        """
        super().__init__(page, timeout)
        self.inventory_logo: Locator = self.page.locator(".app_logo")

        self.products_title: Locator = self.page.locator(".title")

        self.products_filter: Locator = self.page.get_by_role("combobox")
        self.all_filter_options: Locator = self.page.locator("option")
        self.selected_filter_option: Locator = self.page.locator(".active_option")

        self.item: InventoryItem = InventoryItem(page)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)

    def set_products_filter(self, option: str) -> None:
        self.products_filter.select_option(option)

    def add_item_to_cart(self, index: int) -> None:
        item: Locator = self.item.root.nth(index)
        add_button: Locator = item.get_by_role("button", name="Add to cart")
        add_button.click()

    def remove_item_from_cart(self, index: int) -> None:
        item: Locator = self.item.root.nth(index)
        remove_button: Locator = item.get_by_role("button", name="Remove")
        remove_button.click()
