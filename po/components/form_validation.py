from typing import Optional

from playwright.sync_api import Locator, Page

from .base_component import BaseComponent

# Selectors
ERROR_ICON: str = ".error_icon"

# Labels
ERROR_MESSAGE_CONTAINER: str = "Error Message Container"

# CSS
BORDER_BOTTOM_COLOR: str = "border-bottom-color"
BACKGROUND_COLOR: str = "background-color"
COLOR: str = "color"


class FormValidation(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.error_message_container: Locator = self.page.locator(
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
