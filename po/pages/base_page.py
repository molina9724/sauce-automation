from typing import Optional, Union

from playwright.sync_api import Locator
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from ..components.base_component import BaseComponent

BASE_URL: str = "https://www.saucedemo.com/"
LOGIN_URL: str = BASE_URL
INVENTORY_URL: str = BASE_URL + "inventory.html"
CART_URL: str = BASE_URL + "cart.html"
CHECKOUT_STEP_1_URL: str = BASE_URL + "checkout-step-one.html"
CHECKOUT_STEP_2_URL: str = BASE_URL + "checkout-step-two.html"

# Selectors
# FIXME: Items are not global, move them to the right place
ITEM_NAME: str = ".inventory_item_name"
ITEM_PRICE: str = ".inventory_item_price"
ITEM_DESCRIPTION: str = ".inventory_item_desc"
ITEM_QUANTITY: str = ".cart_quantity"
READY_SELECTOR: str = 'input[name="user-name"]'

# Labels
ITEM: str = "Item #"
NAME: str = "Name"
PRICE: str = "Price"
DESCRIPTION: str = "Description"
QUANTITY: str = "Quantity"
REMOVE_BUTTON_LABEL = "Remove Button"

# Buttons
REMOVE: str = "Remove"

# CSS
BORDER_BOTTOM_COLOR: str = "border-bottom-color"
BACKGROUND_COLOR: str = "background-color"
COLOR: str = "color"

# POM
SHORT_TIMEOUT: int = 600
INCREASED_TIMEOUT: int = 20000


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
            return self._page.locator(selector_or_locator)
        else:
            return selector_or_locator

    def goto(
        self,
        url: str,
        ready_selector: Optional[Locator] = None,
        timeout: Optional[int] = None,
    ) -> None:
        """
        Navigates to the specified URL and waits for a specific element to become visible.

        This method loads the given URL, waits for the network to be idle, and then waits for
        a specified selector or locator to be visible on the page. If no selector is provided,
        it defaults to waiting for an input field READY_SELECTOR.

        Args:
            url (str): The URL to navigate to.
            ready_selector (Optional[Union[Locator, str]], optional): The selector or Locator to wait for visibility.
                If not provided, defaults to READY_SELECTOR.
            timeout (Optional[int], optional): Maximum time to wait for navigation and element visibility, in milliseconds.
                If not provided, uses the instance's default timeout.

        Raises:
            RuntimeError: If the specified element does not become visible within the timeout period.
        """
        timeout_ms: int = self._timeout_ms(timeout)
        if ready_selector is not None:
            selector: Locator = self.locator(ready_selector)
        else:
            selector = self.locator(READY_SELECTOR)

        try:
            self._page.goto(url, timeout=timeout_ms)
        except PlaywrightTimeoutError as e:
            raise RuntimeError(
                f"Navigation to {url} timed out after {timeout_ms} ms"
            ) from e

        label = str(selector)
        try:
            self._page.wait_for_load_state("networkidle", timeout=timeout_ms)
            selector.wait_for(state="visible", timeout=timeout_ms)
        except PlaywrightTimeoutError as exception:
            raise RuntimeError(
                f"Timed out waiting for selector {label} to be visible after navigating to {url} (after {timeout_ms} ms)"
            ) from exception

    def get_url(self) -> str:
        return self._page.url
