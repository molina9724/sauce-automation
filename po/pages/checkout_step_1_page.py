from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sauce_project.po.pages.base_page import CART_URL, CHECKOUT_STEP_2_URL, BasePage
from sauce_project.po.pages.cart_page import CartPage

if TYPE_CHECKING:
    from .checkout_step_2_page import CheckoutStepTwoPage

FIRST_NAME_FIELD = "First Name"
LAST_NAME_FIELD = "Last Name"
ZIP_CODE_FIELD = "Zip/Postal Code"

CANCEL_BUTTON_TEXT = "Cancel"
CONTINUE_BUTTON_TEXT = "Continue"

SHORT_TIMEOUT: int = 600


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._checkout_information_wrapper = self.locator(".checkout_info_wrapper")
        self._first_name: Locator = page.get_by_role("textbox", name=FIRST_NAME_FIELD)
        self._last_name: Locator = page.get_by_role("textbox", name=LAST_NAME_FIELD)
        self._zip_code: Locator = page.get_by_role("textbox", name=ZIP_CODE_FIELD)

        self._error_heading: Locator = self.locator("h3[data-test='error']")

        self._cancel_button: Locator = page.get_by_role(
            "button", name=CANCEL_BUTTON_TEXT
        )
        self._continue_button: Locator = page.get_by_role(
            "button", name=CONTINUE_BUTTON_TEXT
        )

    def get_error_text(self, timeout: Optional[int] = None) -> str | None:
        timeout_ms = self._timeout_ms(timeout)
        if self._error_heading.is_visible(timeout=timeout_ms):
            return self._error_heading.inner_text().strip()
        else:
            return None

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

        try:
            self._error_heading.wait_for(state="visible", timeout=SHORT_TIMEOUT)
            error_message = (
                self.get_error_text(SHORT_TIMEOUT) or "Unknown error in checkout"
            )
            raise RuntimeError(error_message)
        except PlaywrightTimeoutError:
            pass

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
        try:
            self._cancel_button.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_cart_page(self, timeout: Optional[int] = None) -> CartPage:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_cancel_button_displayed(timeout=timeout_ms):
            try:
                self._cancel_button.click()
                self.wait_for_url(CART_URL, timeout_ms)
                return CartPage(self._page)
            except RuntimeError:
                raise RuntimeError(
                    f"Timed out waiting for checkout to reach {CART_URL} after {timeout_ms} ms"
                )
        raise RuntimeError(
            f"Timed out waiting for {CANCEL_BUTTON_TEXT} to be displayed after {timeout_ms} ms"
        )
