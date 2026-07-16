from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

# fmt: off
from sauce_project.po.pages.base_page import (CART_URL, CHECKOUT_STEP_2_URL,
                                              BasePage)
# fmt: on
from sauce_project.po.pages.cart_page import CartPage

if TYPE_CHECKING:
    from .checkout_step_2_page import CheckoutStepTwoPage

# Textbox names
FIRST_NAME = "First Name"
LAST_NAME = "Last Name"
ZIP_CODE = "Zip/Postal Code"

# Buttons names
CANCEL_BUTTON = "Cancel"
CONTINUE_BUTTON = "Continue"

# Labels
CANCEL_BUTTON_LABEL: str = "Cancel Button"

SHORT_TIMEOUT: int = 600


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._checkout_information_wrapper: Locator = self.locator(
            ".checkout_info_wrapper"
        )
        self._first_name: Locator = page.get_by_role("textbox", name=FIRST_NAME)
        self._last_name: Locator = page.get_by_role("textbox", name=LAST_NAME)
        self._zip_code: Locator = page.get_by_role("textbox", name=ZIP_CODE)

        self._error_heading: Locator = self.locator('[data-test="error"]')
        self._close_error_button: Locator = self._page.locator(".error-button")

        self._cancel_button: Locator = page.get_by_role("button", name=CANCEL_BUTTON)
        self._continue_button: Locator = page.get_by_role(
            "button", name=CONTINUE_BUTTON
        )

    def is_error_heading_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_heading, timeout_ms)

    def get_error_text(self, timeout: Optional[int] = None) -> str | None:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_error_heading_visible(timeout=timeout_ms):
            return self._error_heading.inner_text().strip()
        else:
            return None

    # TODO: Refactor this method and login (Optional)
    def fill_in_checkout_information(
        self,
        first_name: str,
        last_name: str,
        zip_code: str,
        timeout: Optional[int] = None,
    ) -> "CheckoutStepTwoPage":
        timeout_ms: int = self._timeout_ms(timeout)

        self._first_name.fill(first_name)
        self._last_name.fill(last_name)
        self._zip_code.fill(zip_code)
        self._continue_button.click()

        if self._is_item_displayed(self._error_heading, SHORT_TIMEOUT):
            quick_error_message: str = (
                self.get_error_text(SHORT_TIMEOUT) or "Unknown error in checkout"
            )
            raise RuntimeError(quick_error_message)

        try:
            self._page.wait_for_url(CHECKOUT_STEP_2_URL)
            from .checkout_step_2_page import CheckoutStepTwoPage

            return CheckoutStepTwoPage(self._page)
        except PlaywrightTimeoutError:
            error_message: str | None = self.get_error_text(SHORT_TIMEOUT)
            if error_message:
                raise RuntimeError(error_message)
            raise RuntimeError(
                f"Timed out waiting for checkout to reach {CHECKOUT_STEP_2_URL} after {timeout_ms} ms"
            )

    def is_cancel_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._cancel_button, timeout_ms)

    def get_cart_page(self, timeout: Optional[int] = None) -> CartPage:
        timeout_ms: int = self._timeout_ms(timeout)
        cancel_button = self.get_element(
            self._cancel_button, CANCEL_BUTTON_LABEL, timeout_ms
        )
        cancel_button.click()
        try:
            self.wait_for_url(CART_URL, timeout_ms)
            return CartPage(self._page)
        except RuntimeError:
            raise RuntimeError(
                f"Timed out waiting for checkout to reach {CART_URL} after {timeout_ms} ms"
            )
