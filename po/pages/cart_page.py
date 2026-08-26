from typing import TYPE_CHECKING, List

from playwright.sync_api import Locator, Page

from ..components.cart import Cart
from ..components.cart_page_item import CartItem
from ..components.left_menu import Menu
# fmt: off
from .base_page import BasePage
# fmt: on
from .inventory_page import InventoryPage

if TYPE_CHECKING:
    from .checkout_step_1_page import CheckoutStepOnePage


class CartPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.item: CartItem = CartItem(page)

        self.continue_shopping_button: Locator = self.page.get_by_role(
            "button", name="Continue Shopping"
        )
        self.checkout_button: Locator = self.page.get_by_role("button", name="Checkout")
        self.cart: Cart = Cart(self.page)
        self.menu: Menu = Menu(self.page)

    def get_all_products_quantities(self) -> List[str]:
        return self.item.quantity.all_inner_texts()

    def get_all_products_information(self) -> dict[str, dict[str, str]]:
        all_inventory_items_names: List[str] = self.item.get_all_products_names()
        all_inventory_items_descriptions: List[str] = (
            self.item.get_all_products_descriptions()
        )
        all_inventory_items_prices: List[str] = self.item.get_all_products_prices()
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
        self.item.remove_button.nth(index).click()

    def get_inventory_page(self) -> InventoryPage:
        self.continue_shopping_button.click()
        return InventoryPage(self.page)

    def get_checkout_step_1_page(self) -> "CheckoutStepOnePage":
        self.checkout_button.click()
        from .checkout_step_1_page import CheckoutStepOnePage

        return CheckoutStepOnePage(self.page)
