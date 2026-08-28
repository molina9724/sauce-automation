from decimal import Decimal
from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from po.components.cart_page_item import CartItem

from ..components.cart import Cart
from ..components.left_menu import Menu
from ..pages.base_page import BasePage

TAXES: Decimal = Decimal("0.08")
CURRENCY = "$"

SUBTOTAL: str = "Subtotal"
TAX: str = "Tax"
TOTAL: str = "Total"


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.cart_list: Locator = self.locator(".cart_list")

        self.subtotal: Locator = self.locator(".summary_subtotal_label")
        self.tax: Locator = self.locator(".summary_tax_label")
        self.total: Locator = self.locator(".summary_total_label")

        self.item: CartItem = CartItem(page)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)

    def is_cart_list_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self.cart_list.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def _extract_currency_value(self, locator: Locator, label: str) -> str:
        value: str = locator.inner_text().strip()
        currency_index: int = value.find(CURRENCY)

        if currency_index != -1:
            cleaned_value: str = value[currency_index:]
            return cleaned_value
        else:
            raise RuntimeError(f"{label} doesn't have a currency")

    def get_subtotal(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_element(self.subtotal, SUBTOTAL, timeout_ms)
        return self._extract_currency_value(self.subtotal, SUBTOTAL)

    def get_tax(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(self.tax, timeout_ms):
            return self._extract_currency_value(self.tax, TAX)
        raise RuntimeError(
            f"Timed out waiting for {TAX} to be displayed after {timeout_ms} ms"
        )

    def get_total(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(self.total, timeout_ms):
            return self._extract_currency_value(self.total, TOTAL)
        raise RuntimeError(
            f"Timed out waiting for {TOTAL} to be displayed after {timeout_ms} ms"
        )
