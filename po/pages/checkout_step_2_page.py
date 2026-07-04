from decimal import Decimal
from typing import List, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sauce_project.po.pages.base_page import BasePage

TAXES: Decimal = Decimal("0.08")
CURRENCY = "$"


class CheckoutStepTwoPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._cart_list: Locator = self.locator(".cart_list")

        self._cart_item: Locator = self.locator(".cart_item")
        self._item_quantity: Locator = self.locator(".cart_quantity")
        self._item_name: Locator = self.locator(".inventory_item_name")
        self._item_description: Locator = self.locator(".inventory_item_desc")
        self._item_price: Locator = self.locator(".inventory_item_price")

    def is_cart_list_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_list.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def calculate_item_total(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_visible(timeout=timeout_ms):
            all_products_price: List[str] = [
                item.inner_text().strip() for item in self._item_price.all()
            ]
            all_products_price_without_currency: List[Decimal] = [
                Decimal(price[1:]) for price in all_products_price
            ]
            total: Decimal = sum(all_products_price_without_currency, Decimal("0"))
            return f"{CURRENCY}{total:.2f}"
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )

    def calculate_taxes(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cart_list_visible(timeout=timeout_ms):
            total: str = self.calculate_item_total()
            total_without_currency = Decimal(total[1:])
            taxes: Decimal = round(total_without_currency * TAXES, 2)
            return f"{CURRENCY}{taxes:.2f}"
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )
