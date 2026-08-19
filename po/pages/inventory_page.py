from typing import List, Optional

from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.left_menu import Menu
from .base_page import ITEM, ITEM_DESCRIPTION, ITEM_NAME, ITEM_PRICE, REMOVE, BasePage

# Buttons
ADD_TO_CART: str = "Add to cart"

# Labels
ITEMS_CONTAINER: str = "Items Container"
PRODUCTS_FILTER: str = "Products Filter"
PRODUCTS_TITLE: str = "Products Title"


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

        self.all_items_container: Locator = self.page.locator(".inventory_list")
        self.item: Locator = self.page.locator(".inventory_item")
        self.item_name: Locator = self.item.locator(ITEM_NAME)
        self.item_description: Locator = self.item.locator(ITEM_DESCRIPTION)
        self.item_price: Locator = self.item.locator(ITEM_PRICE)
        self.item_image: Locator = self.item.locator("img[class='inventory_item_img']")
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)

    def set_products_filter(self, option: str) -> None:
        self.products_filter.select_option(option)

    # get_all_products_names, get_all_products_descriptions, get_all_products_prices aren't refactored since data might change in the future
    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        names: List[str] = []
        for index, item in enumerate(self.item.all()):
            name: Locator = self.get_element(
                item.locator(ITEM_NAME),
                f"{ITEM_NAME} for {ITEM}{index}",
                timeout_ms,
            )
            names.append(name.inner_text().strip())
        return names

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        descriptions: List[str] = []
        for index, item in enumerate(self.item.all()):
            description: Locator = self.get_element(
                item.locator(ITEM_DESCRIPTION),
                f"{ITEM_DESCRIPTION} for {ITEM}{index}",
                timeout_ms,
            )
            descriptions.append(description.inner_text().strip())
        return descriptions

    def get_all_products_prices(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        prices: List[str] = []
        for index, item in enumerate(self.item.all()):
            price: Locator = self.get_element(
                item.locator(ITEM_PRICE), f"{ITEM_PRICE} for {ITEM}{index}", timeout_ms
            )
            prices.append(price.inner_text().strip())
        return prices

    # TODO: This method should include images and add/remove buttons to consistently test the whole item object
    # TODO: Investigate how to to test images properly
    def get_all_products_information(
        self, timeout: Optional[int] = None
    ) -> dict[str, dict[str, str]]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_inventory_items_names: List[str] = self.get_all_products_names(timeout_ms)
        all_inventory_items_descriptions: List[str] = (
            self.get_all_products_descriptions(timeout_ms)
        )
        all_inventory_items_prices: List[str] = self.get_all_products_prices(timeout_ms)

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
        item: Locator = self.item.nth(index)
        add_button: Locator = item.get_by_role("button", name=ADD_TO_CART)
        add_button.click()

    def remove_item_from_cart(self, index: int) -> None:
        item: Locator = self.item.nth(index)
        remove_button: Locator = item.get_by_role("button", name=REMOVE)
        remove_button.click()
