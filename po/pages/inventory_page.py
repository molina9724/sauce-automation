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

    # TODO: This method should include images and add/remove buttons to consistently test the whole item object
    # TODO: Investigate how to to test images properly
    def get_all_products_information(self) -> dict[str, dict[str, str]]:
        all_inventory_items_names: list[str] = self.item.get_all_products_names()
        all_inventory_items_descriptions: list[str] = (
            self.item.get_all_products_descriptions()
        )
        all_inventory_items_prices: list[str] = self.item.get_all_products_prices()

        inventory_items_data: dict[str, dict[str, str]] = dict()
        try:
            for name, description, price in zip(
                all_inventory_items_names,
                all_inventory_items_descriptions,
                all_inventory_items_prices,
                strict=True,
            ):
                inventory_items_data[name] = {
                    "description": description,
                    "price": price,
                }
            return inventory_items_data
        except ValueError as exception:
            raise RuntimeError(
                "The arguments (name, description, and price) for zip have different lengths, this means that some inventory items have missing properties."
            ) from exception

    def add_item_to_cart(self, index: int) -> None:
        item: Locator = self.item.root.nth(index)
        add_button: Locator = item.get_by_role("button", name="Add to cart")
        add_button.click()

    def remove_item_from_cart(self, index: int) -> None:
        item: Locator = self.item.root.nth(index)
        remove_button: Locator = item.get_by_role("button", name="Remove")
        remove_button.click()
