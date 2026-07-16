from typing import Optional, Union

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

BASE_URL: str = "https://www.saucedemo.com/"
LOGIN_URL: str = BASE_URL
INVENTORY_URL: str = BASE_URL + "inventory.html"
CART_URL: str = BASE_URL + "cart.html"
CHECKOUT_STEP_1_URL: str = BASE_URL + "checkout-step-one.html"
CHECKOUT_STEP_2_URL: str = BASE_URL + "checkout-step-two.html"

# Selectors
ITEM_NAME: str = ".inventory_item_name"
ITEM_PRICE: str = ".inventory_item_price"
ITEM_DESCRIPTION: str = ".inventory_item_desc"
CART_BUTTON: str = ".shopping_cart_link"
CART_COUNTER_BADGE: str = ".shopping_cart_badge"
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


class BasePage:
    """
    A base class for page objects in UI automation frameworks.

    This class provides common functionality for interacting with web pages,
    such as managing the Playwright Page instance and handling locators.

    Attributes:
        _page (Page): The Playwright Page instance used for browser interactions.
        _timeout (int): Default timeout (in milliseconds) for page actions.

    Args:
        page (Page): The Playwright Page object to interact with.
        timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
    """

    def __init__(self, page: Page, timeout: int = 10000) -> None:
        """
        Initializes the BasePage with a Playwright Page instance and an optional timeout.

        Args:
            page (Page): The Playwright Page object to interact with.
            timeout (int, optional): Default timeout for actions, in milliseconds. Defaults to 10000.
        """
        self._page: Page = page
        self._timeout: int = timeout
        self._cart_button: Locator = self._page.locator(CART_BUTTON)
        self._cart_counter: Locator = self._cart_button.locator(CART_COUNTER_BADGE)

    def _timeout_ms(self, timeout: Optional[int]) -> int:
        """Resolve an optional timeout argument to an int (milliseconds).

        This centralizes the common pattern of using an explicit timeout when
        provided or falling back to the instance default. Use this from page
        object methods instead of repeating the conditional everywhere.
        """
        return timeout if timeout is not None else self._timeout

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

    def wait_for_url(self, expected_url: str, timeout: Optional[int] = None) -> None:
        """Wait until the page URL matches expected_url within timeout.

        Raises RuntimeError on timeout to keep behavior consistent with other waits.
        """
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._page.wait_for_url(expected_url, timeout=timeout_ms)
        except PlaywrightTimeoutError as e:
            raise RuntimeError(
                f"Timed out waiting for URL {expected_url} after {timeout_ms} ms"
            ) from e

    def get_url(self) -> str:
        return self._page.url

    def _is_item_displayed(
        self, locator: Locator, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            locator.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_element(
        self, locator: Locator, label: str, timeout: Optional[int] = None
    ) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._is_item_displayed(locator, timeout_ms):
            return locator
        raise RuntimeError(
            f"Timed out waiting for {label} to be displayed after {timeout_ms} ms"
        )

    def is_cart_empty(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._cart_counter.wait_for(state="hidden", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False
