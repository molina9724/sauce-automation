from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator

from sauce_project.po.pages.base_page import BasePage

if TYPE_CHECKING:
    _Base = BasePage
else:
    _Base = object

# Selectors
ERROR_ICON: str = ".error_icon"

# Labels
ERROR_MESSAGE_CONTAINER: str = "Error Message Container"
ERROR_HEADING: str = "Error Heading"


class FormValidationMixIn(_Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
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

    def is_error_heading_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_heading, timeout_ms)

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
        if self.is_error_heading_visible(timeout=timeout_ms):
            return self._error_heading.inner_text().strip()
        else:
            return None
