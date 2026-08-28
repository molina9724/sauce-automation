from typing import Union

from playwright.sync_api import Locator

from ..components.base_component import BaseComponent

BASE_URL: str = "https://www.saucedemo.com/"
LOGIN_URL: str = BASE_URL
INVENTORY_URL: str = BASE_URL + "inventory.html"
CART_URL: str = BASE_URL + "cart.html"
CHECKOUT_STEP_1_URL: str = BASE_URL + "checkout-step-one.html"
CHECKOUT_STEP_2_URL: str = BASE_URL + "checkout-step-two.html"

# Selectors
READY_SELECTOR: str = "#root"


class BasePage(BaseComponent):
    def locator(self, selector_or_locator: Union[str, Locator]) -> Locator:
        """
        Returns a Playwright Locator object for the given selector or locator.

        Args:
            selector_or_locator (Union[str, Locator]): A CSS selector string or an existing Locator object.

        Returns:
            Locator: A Playwright Locator object corresponding to the selector or the provided Locator.
        """
        if isinstance(selector_or_locator, str):
            return self.page.locator(selector_or_locator)
        else:
            return selector_or_locator
