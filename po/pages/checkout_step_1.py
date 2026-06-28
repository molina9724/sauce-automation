from playwright.sync_api import Locator, Page

from sauce_project.po.pages.base_page import BasePage

FIRST_NAME_FIELD = "First Name"
LAST_NAME_FIELD = "Last Name"
ZIP_CODE_FIELD = "Zip/Postal Code"

CANCEL_BUTTON_TEXT = "Cancel"
CONTINUE_BUTTON_TEXT = "Continue"


class CheckoutStepOnePage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._checkout_information_wrapper = self.locator(".checkout_info_wrapper")
        self._first_name: Locator = page.get_by_role("textbox", name=FIRST_NAME_FIELD)
        self._last_name: Locator = page.get_by_role("textbox", name=LAST_NAME_FIELD)
        self._zip_code: Locator = page.get_by_role("textbox", name=ZIP_CODE_FIELD)

        self._cancel_button: Locator = page.get_by_role(
            "button", name=CANCEL_BUTTON_TEXT
        )
        self._continue_button: Locator = page.get_by_role(
            "button", name=CONTINUE_BUTTON_TEXT
        )
