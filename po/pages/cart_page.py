from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page

# fmt: off
from .base_page import (DESCRIPTION, ITEM, ITEM_DESCRIPTION, ITEM_NAME,
                        ITEM_PRICE, ITEM_QUANTITY, NAME, PRICE, QUANTITY,
                        BasePage)
# fmt: on
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


# Labels
REMOVE_BUTTON_LABEL = "Remove Button"

# Button names
REMOVE = "Remove"
CONTINUE_SHOPPING = "Continue Shopping"
CHECKOUT = "Checkout"

SHORT_TIMEOUT = 600


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._cart_list: Locator = self.locator(".cart_list")

        self._item_object: Locator = self.locator(".cart_item")
        self._item_quantity: Locator = self._item_object.locator(ITEM_QUANTITY)
        self._item_name: Locator = self._item_object.locator(ITEM_NAME)
        self._item_description: Locator = self._item_object.locator(ITEM_DESCRIPTION)
        self._item_price: Locator = self._item_object.locator(ITEM_PRICE)
        self._remove_item_button: Locator = self._item_object.get_by_role(
            "button", name=REMOVE
        )

        self._continue_shopping_button: Locator = self._page.get_by_role(
            "button", name=CONTINUE_SHOPPING
        )
        self._checkout_button: Locator = self._page.get_by_role("button", name=CHECKOUT)

    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_names: List[str] = list()
        for index, item in enumerate(self._item_object.all()):
            name: Locator = self.get_element(
                item.locator(ITEM_NAME), f"{NAME} for {ITEM}{index}", timeout_ms
            )
            all_products_names.append(name.inner_text().strip())
        return all_products_names

    def get_all_products_quantities(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_quantities: List[str] = list()
        for index, item in enumerate(self._item_object.all()):
            quantity: Locator = self.get_element(
                item.locator(ITEM_QUANTITY), f"{QUANTITY} for {ITEM}{index}", timeout_ms
            )
            all_products_quantities.append(quantity.inner_text().strip())
        return all_products_quantities

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        all_products_descriptions: List[str] = list()
        for index, item in enumerate(self._item_object.all()):
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
        for index, item in enumerate(self._item_object.all()):
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

    def remove_item(self, index: int = 0, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        remove_button: Locator = self.get_element(
            self._remove_item_button.nth(index),
            f"{REMOVE_BUTTON_LABEL} for {ITEM}{index}",
            timeout_ms,
        )
        remove_button.click()

    def get_amount_of_items_in_cart(self, timeout: Optional[int] = None) -> int:
        if timeout is None:
            timeout_ms: int = SHORT_TIMEOUT
        else:
            timeout_ms = self._timeout_ms(timeout)
        try:
            self.get_element(self._item_object.first, ITEM, timeout_ms)
            return self._item_object.count()
        except RuntimeError:
            return 0

    def is_continue_shopping_button_displayed(
        self, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._continue_shopping_button, timeout_ms)

    def get_inventory_page(self, timeout: Optional[int] = None) -> InventoryPage:
        timeout_ms: int = self._timeout_ms(timeout)
        continue_shopping_button: Locator = self.get_element(
            self._continue_shopping_button, CONTINUE_SHOPPING, timeout_ms
        )
        continue_shopping_button.click()
        return InventoryPage(self._page)

    def is_checkout_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._checkout_button, timeout_ms)

    def get_checkout_step_1_page(
        self, timeout: Optional[int] = None
    ) -> "CheckoutStepOnePage":
        timeout_ms: int = self._timeout_ms(timeout)
        checkout_button: Locator = self.get_element(
            self._checkout_button, CHECKOUT, timeout_ms
        )
        checkout_button.click()
        from .checkout_step_1_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self._page)
