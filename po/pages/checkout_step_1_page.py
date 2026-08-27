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


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.first_name: Locator = page.get_by_role("textbox", name=FIRST_NAME)
        self.last_name: Locator = page.get_by_role("textbox", name=LAST_NAME)
        self.zip_code: Locator = page.get_by_role("textbox", name=ZIP_CODE)

        self.cancel_button: Locator = page.get_by_role("button", name=CANCEL_BUTTON)
        self.continue_button: Locator = page.get_by_role("button", name=CONTINUE_BUTTON)
        self.menu: Menu = Menu(self.page)
        self.cart: Cart = Cart(self.page)
        self.form_validation: FormValidation = FormValidation(self.page)

    def get_fields(self) -> tuple[Locator, Locator, Locator]:
        return self.first_name, self.last_name, self.zip_code

    def get_fields_containers(self) -> tuple[Locator, Locator, Locator]:
        # The error icon is a sibling of the field, not a child of it
        return (
            self.get_parent(self.first_name),
            self.get_parent(self.last_name),
            self.get_parent(self.zip_code),
        )

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

    def cancel(self) -> CartPage:
        self.cancel_button.click()
        return CartPage(self.page)
