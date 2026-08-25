from typing import TYPE_CHECKING, List

from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.left_menu import Menu
# fmt: off
from .base_page import (ITEM_DESCRIPTION, ITEM_NAME, ITEM_PRICE, ITEM_QUANTITY,
                        REMOVE, BasePage)
# fmt: on
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.item: Locator = self.locator(".cart_item")
        self.item_quantity: Locator = self.item.locator(ITEM_QUANTITY)
        self.item_name: Locator = self.item.locator(ITEM_NAME)
        self.item_description: Locator = self.item.locator(ITEM_DESCRIPTION)
        self.item_price: Locator = self.item.locator(ITEM_PRICE)
        self.remove_item_button: Locator = self.item.get_by_role("button", name=REMOVE)

        self.continue_shopping_button: Locator = self.page.get_by_role(
            "button", name="Continue Shopping"
        )
        self.checkout_button: Locator = self.page.get_by_role("button", name="Checkout")
        self.cart: Cart = Cart(self.page)
        self.menu: Menu = Menu(self.page)

    def get_all_products_names(self) -> List[str]:
        return self.item_name.all_inner_texts()

    def get_all_products_quantities(self) -> List[str]:
        return self.item_quantity.all_inner_texts()

    def get_all_products_descriptions(self) -> List[str]:
        return self.item_description.all_inner_texts()

    def get_all_products_prices(self) -> List[str]:
        return self.item_price.all_inner_texts()

    def get_all_products_information(self) -> dict[str, dict[str, str]]:
        all_inventory_items_names: List[str] = self.get_all_products_names()
        all_inventory_items_descriptions: List[str] = (
            self.get_all_products_descriptions()
        )
        all_inventory_items_prices: List[str] = self.get_all_products_prices()
        all_inventory_items_quantities: List[str] = self.get_all_products_quantities()

        inventory_items_data: dict[str, dict[str, str]] = dict()
        try:
            for name, description, price, quantity in zip(
                all_inventory_items_names,
                all_inventory_items_descriptions,
                all_inventory_items_prices,
                all_inventory_items_quantities,
                strict=True,
            ):
                inventory_items_data[name] = {
                    "description": description,
                    "price": price,
                    "quantity": quantity,
                }
            return inventory_items_data
        except ValueError as exception:
            raise RuntimeError(
                "The arguments (name, description, price, and quantity) have different lengths, this means that some inventory items have missing properties."
            ) from exception

    def remove_item(self, index: int = 0) -> None:
        self.remove_item_button.nth(index).click()

    def get_inventory_page(self) -> InventoryPage:
        self.continue_shopping_button.click()
        return InventoryPage(self.page)

    def get_checkout_step_1_page(self) -> "CheckoutStepOnePage":
        self.checkout_button.click()
        from .checkout_step_1_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self.page)
