from typing import TYPE_CHECKING, List, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage

REMOVE_BUTTON_NAME = "Remove"
CONTINUE_SHOPPING_BUTTON_NAME = "Continue Shopping"
CHECKOUT_BUTTON_NAME = "Checkout"


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._cart_list: Locator = self.locator(".cart_list")

        self._item_object: Locator = self.locator(".cart_item")
        self._item_quantity: Locator = self.locator(".cart_quantity")
        self._item_name: Locator = self.locator(".inventory_item_name")
        self._item_description: Locator = self.locator(".inventory_item_desc")
        self._item_price: Locator = self.locator(".inventory_item_price")
        self._remove_item_button: Locator = page.get_by_role(
            "button", name=REMOVE_BUTTON_NAME
        )

        self._continue_shopping_button: Locator = page.get_by_role(
            "button", name=CONTINUE_SHOPPING_BUTTON_NAME
        )
        self._checkout_button: Locator = page.get_by_role(
            "button", name=CHECKOUT_BUTTON_NAME
        )

    def is_cart_list_container_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_list.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_cart_empty(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._item_object.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_all_products_quantities(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_container_displayed(timeout=timeout_ms):
            all_products_quantity: List[str] = [
                item.inner_text().strip() for item in self._item_quantity.all()
            ]
            return all_products_quantity
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_names(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_container_displayed(timeout=timeout_ms):
            all_products_names: List[str] = [
                item.inner_text().strip() for item in self._item_name.all()
            ]
            return all_products_names
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_descriptions(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_container_displayed(timeout=timeout_ms):
            all_products_descriptions: List[str] = [
                item.inner_text().strip() for item in self._item_description.all()
            ]
            return all_products_descriptions
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )

    def get_all_products_prices(self, timeout: Optional[int] = None) -> List[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_container_displayed(timeout=timeout_ms):
            all_products_price: List[str] = [
                item.inner_text().strip() for item in self._item_price.all()
            ]
            return all_products_price
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )

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
                "The arguments (name, description, price, and quantity) for zip have different lengths, this means that some inventory items have missing properties."
            ) from exception

    def remove_item(self, index: int = 0, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._remove_item_button.wait_for(state="visible", timeout=timeout_ms)
            self._remove_item_button.nth(index).click()
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for remove button for item #{index} to be displayed (after {timeout_ms} ms)"
            )

    def get_amount_of_items_in_cart(self, timeout: Optional[int] = None) -> int:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_container_displayed(timeout_ms):
            index = 0
            try:
                all_items: List[Locator] = self._item_object.all()
                for index, item in enumerate(all_items):
                    item.wait_for(state="visible", timeout=timeout_ms)
            except PlaywrightTimeoutError:
                raise RuntimeError(
                    f"Timed out waiting for item #{index} to be displayed (after {timeout_ms} ms)"
                )
            else:
                return len(all_items)
        return 0

    def is_continue_shopping_button_displayed(
        self, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._continue_shopping_button.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_inventory_page(self, timeout: Optional[int] = None) -> InventoryPage:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._continue_shopping_button.click(timeout=timeout_ms)
            return InventoryPage(self._page)
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for {CONTINUE_SHOPPING_BUTTON_NAME} button to be clicked (after {timeout_ms} ms)"
            )

    def is_checkout_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._checkout_button.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_checkout_step_1_page(
        self, timeout: Optional[int] = None
    ) -> "CheckoutStepOnePage":
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._checkout_button.click(timeout=timeout_ms)
            from .checkout_step_1_page import CheckoutStepOnePage

            return CheckoutStepOnePage(self._page)
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for {CHECKOUT_BUTTON_NAME} button to be clicked (after {timeout_ms} ms)"
            )
