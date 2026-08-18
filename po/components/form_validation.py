from typing import Optional

from playwright.sync_api import Locator, Page

from .base_component import BaseComponent

# Selectors
ERROR_ICON: str = ".error_icon"

# Labels
ERROR_MESSAGE_CONTAINER: str = "Error Message Container"


class FormValidation(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.error_message_container: Locator = self._page.locator(
            ".error-message-container.error"
        )
        self.error_heading: Locator = self.error_message_container.locator(
            "h3[data-test='error']"
        )

    def get_error_message_container(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        error_message_container: Locator = self.get_element(
            self.error_message_container, ERROR_MESSAGE_CONTAINER, timeout_ms
        )
        return error_message_container

    # TODO: Remove on checkout_step_1_page refactor
    def get_error_text(self, timeout: Optional[int] = None) -> str | None:
        if self.error_heading.is_visible():
            return self.error_heading.inner_text().strip()
        else:
            return None

    # TODO: Remove on checkout_step_1_page refactor
    def is_error_heading_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self.error_heading, timeout_ms)
