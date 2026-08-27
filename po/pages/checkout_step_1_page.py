from typing import Optional

from playwright.sync_api import Locator, Page

from po.pages.cart_page import CartPage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage

from ..components.cart import Cart
from ..components.form_validation import FormValidation
from ..components.left_menu import Menu
from ..pages.base_page import CHECKOUT_STEP_2_URL, BasePage

# Textbox names
FIRST_NAME = "First Name"
LAST_NAME = "Last Name"
ZIP_CODE = "Zip/Postal Code"

# Buttons names
CANCEL_BUTTON = "Cancel"
CONTINUE_BUTTON = "Continue"

# Labels
CANCEL_BUTTON_LABEL: str = "Cancel Button"
FIRST_NAME_LABEL = "First Name Field"
LAST_NAME_LABEL = "Last Name Field"
ZIP_CODE_LABEL = "Zip/Postal Code Field"


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.checkout_information_wrapper: Locator = self.locator(
            ".checkout_info_wrapper"
        )
        self.first_name: Locator = page.get_by_role("textbox", name=FIRST_NAME)
        self.last_name: Locator = page.get_by_role("textbox", name=LAST_NAME)
        self.zip_code: Locator = page.get_by_role("textbox", name=ZIP_CODE)

        self.cancel_button: Locator = page.get_by_role("button", name=CANCEL_BUTTON)
        self.continue_button: Locator = page.get_by_role("button", name=CONTINUE_BUTTON)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)
        self.form_validation: FormValidation = FormValidation(self.page)

    def get_first_name_object(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        first_name: Locator = self.get_element(
            self.first_name, FIRST_NAME_LABEL, timeout_ms
        )
        return first_name

    def get_last_name_object(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        last_name: Locator = self.get_element(
            self.last_name, LAST_NAME_LABEL, timeout_ms
        )
        return last_name

    def get_zip_code_object(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        zip_code: Locator = self.get_element(self.zip_code, ZIP_CODE_LABEL, timeout_ms)
        return zip_code

    def get_fields(self) -> tuple[Locator, Locator, Locator]:
        first_name: Locator = self.get_first_name_object()
        last_name: Locator = self.get_last_name_object()
        zip_code: Locator = self.get_zip_code_object()

        return first_name, last_name, zip_code

    def get_fields_containers(self) -> tuple[Locator, Locator, Locator]:
        first_name, last_name, zip_code = self.get_fields()

        # The error icon is a sibling of the field, not a child of it
        first_name_parent: Locator = self.get_parent(first_name)
        last_name_parent: Locator = self.get_parent(last_name)
        zip_code_parent: Locator = self.get_parent(zip_code)

        return first_name_parent, last_name_parent, zip_code_parent

    # TODO: Refactor this method and login (Optional)
    def fill_in_checkout_information(
        self,
        first_name: str,
        last_name: str,
        zip_code: str,
    ) -> None:
        self.first_name.fill(first_name)
        self.last_name.fill(last_name)
        self.zip_code.fill(zip_code)
        self.continue_button.click()

    def get_checkout_step_two_page(self) -> CheckoutStepTwoPage:
        self.page.wait_for_url(CHECKOUT_STEP_2_URL)

        from .checkout_step_2_page import CheckoutStepTwoPage

        return CheckoutStepTwoPage(self.page)

    def is_cancel_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self.cancel_button, timeout_ms)

    def cancel(self) -> CartPage:
        self.cancel_button.click()
        return CartPage(self.page)
