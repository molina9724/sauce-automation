from playwright.sync_api import Locator, Page

from .base_component import BaseComponent

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
