from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.left_menu import Menu
# fmt: off
from .base_page import (DESCRIPTION, ITEM, ITEM_DESCRIPTION, ITEM_NAME,
                        ITEM_PRICE, ITEM_QUANTITY, NAME, PRICE, QUANTITY,
                        REMOVE, REMOVE_BUTTON_LABEL, SHORT_TIMEOUT, BasePage)
# fmt: on
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


# Button names
CONTINUE_SHOPPING = "Continue Shopping"
CHECKOUT = "Checkout"


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
            "button", name=CONTINUE_SHOPPING
        )
        self.checkout_button: Locator = self.page.get_by_role("button", name=CHECKOUT)
        self.cart: Cart = Cart(self.page)
        self.menu: Menu = Menu(self.page)

    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_names: List[str] = list()
        for index, item in enumerate(self.item.all()):
            name: Locator = self.get_element(
                item.locator(ITEM_NAME), f"{NAME} for {ITEM}{index}", timeout_ms
            )
            all_products_names.append(name.inner_text().strip())
        return all_products_names

    def get_all_products_quantities(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_quantities: List[str] = list()
        for index, item in enumerate(self.item.all()):
            quantity: Locator = self.get_element(
                item.locator(ITEM_QUANTITY), f"{QUANTITY} for {ITEM}{index}", timeout_ms
            )
            all_products_quantities.append(quantity.inner_text().strip())
        return all_products_quantities

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_descriptions: List[str] = list()
        for index, item in enumerate(self.item.all()):
            description: Locator = self.get_element(
                item.locator(ITEM_DESCRIPTION),
                f"{DESCRIPTION} for {ITEM}{index}",
                timeout_ms,
            )
            all_products_descriptions.append(description.inner_text().strip())
        return all_products_descriptions

    def get_all_products_prices(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_prices: List[str] = list()
        for index, item in enumerate(self.item.all()):
            price: Locator = self.get_element(
                item.locator(ITEM_PRICE), f"{PRICE} for {ITEM}{index}", timeout_ms
            )
            all_products_prices.append(price.inner_text().strip())
        return all_products_prices

    def get_all_products_information(
        self, timeout: Optional[int] = None
    ) -> dict[str, dict[str, str]]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_inventory_items_names: List[str] = self.get_all_products_names(timeout_ms)
        all_inventory_items_descriptions: List[str] = (
            self.get_all_products_descriptions(timeout_ms)
        )
        all_inventory_items_prices: List[str] = self.get_all_products_prices(timeout_ms)
        all_inventory_items_quantities: List[str] = self.get_all_products_quantities(
            timeout_ms
        )

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
