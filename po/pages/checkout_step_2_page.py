from decimal import Decimal
from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sauce_project.po.pages.base_page import BasePage

TAXES: Decimal = Decimal("0.08")
CURRENCY = "$"

SUBTOTAL: str = "Subtotal"
TAX: str = "Tax"
TOTAL: str = "Total"


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._cart_list: Locator = self.locator(".cart_list")

        self._cart_item: Locator = self.locator(".cart_item")
        self._item_quantity: Locator = self.locator(".cart_quantity")
        self._item_name: Locator = self.locator(".inventory_item_name")
        self._item_description: Locator = self.locator(".inventory_item_desc")
        self._item_price: Locator = self.locator(".inventory_item_price")

        self._subtotal: Locator = self.locator(".summary_subtotal_label")
        self._tax: Locator = self.locator(".summary_tax_label")
        self._total: Locator = self.locator(".summary_total_label")

    def is_cart_list_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_list.wait_for(state="visible", timeout=timeout_ms)
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

    def _is_item_displayed(
        self, locator: Locator, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_subtotal(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(self._subtotal, timeout_ms):
            return self._extract_currency_value(self._subtotal, SUBTOTAL)
        raise RuntimeError(
            f"Timed out waiting for {SUBTOTAL} to be displayed after {timeout_ms} ms"
        )

    def get_tax(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(self._tax, timeout_ms):
            return self._extract_currency_value(self._tax, TAX)
        raise RuntimeError(
            f"Timed out waiting for {TAX} to be displayed after {timeout_ms} ms"
        )

    def get_total(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(self._total, timeout_ms):
            return self._extract_currency_value(self._total, TOTAL)
        raise RuntimeError(
            f"Timed out waiting for {TOTAL} to be displayed after {timeout_ms} ms"
        )
