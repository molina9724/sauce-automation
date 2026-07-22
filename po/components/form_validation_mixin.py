from typing import TYPE_CHECKING

from playwright.sync_api import Locator

from sauce_project.po.pages.base_page import BasePage

if TYPE_CHECKING:
    _Base = BasePage
else:
    _Base = object

# Selectors
ERROR_ICON: str = ".error_icon"


class FormValidationMixIn(_Base):
    def __init__(self, *args, **kwargs) -> None:
        super().__init__(*args, **kwargs)
        self._error_message_container: Locator = self._page.locator(
            ".error-message-container.error"
        )
        self._error_heading: Locator = self._error_message_container.locator(
            "h3[data-test='error']"
        )
