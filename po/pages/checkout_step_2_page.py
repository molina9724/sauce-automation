from typing import List, Optional

from playwright.sync_api import Locator, Page

from sauce_project.po.pages.base_page import BasePage

TAXES: float = 0.08
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

    def calculate_item_total(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._cart_list.is_visible(timeout=timeout_ms):
            all_products_price: List[str] = [
                item.inner_text().strip() for item in self._item_price.all()
            ]
            all_products_price_without_currency: List[float] = [
                float(price[1:]) for price in all_products_price
            ]
            total_with_currency: str = CURRENCY + str(
                sum(all_products_price_without_currency)
            )
            return total_with_currency
        raise RuntimeError(
            f"Timed out waiting for car list container to be displayed (after {timeout_ms} ms)"
        )
