from typing import Optional

from playwright.sync_api import Locator, Page

from .base_component import BaseComponent

# Selectors
ERROR_ICON: str = ".error_icon"

# Labels
ERROR_MESSAGE_CONTAINER: str = "Error Message Container"
ERROR_HEADING: str = "Error Heading"


class FormValidation(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._error_message_container: Locator = self._page.locator(
            ".error-message-container.error"
        )
        self._error_heading: Locator = self._error_message_container.locator(
            "h3[data-test='error']"
        )

    def is_error_container_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_message_container, timeout_ms)

    def get_error_message_container(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        error_message_container: Locator = self.get_element(
            self._error_message_container, ERROR_MESSAGE_CONTAINER, timeout_ms
        )
        return error_message_container

    def is_error_heading_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_heading, timeout_ms)

    def is_error_heading_hidden(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_hidden(self._error_heading, timeout_ms)

    def get_error_heading(self, timeout: Optional[int] = None) -> Locator:
        timeout_ms: int = self._timeout_ms(timeout)
        error_heading: Locator = self.get_element(
            self._error_heading, ERROR_HEADING, timeout_ms
        )
        return error_heading

    def is_error_displayed(self, timeout: Optional[int] = None) -> bool:
        if timeout is None:
            return self._error_heading.is_visible()
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_heading, timeout_ms)

    def get_error_text(self, timeout: Optional[int] = None) -> str | None:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_error_heading_displayed(timeout=timeout_ms):
            return self._error_heading.inner_text().strip()
        else:
            return None
