from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sauce_project.data.login_data import PERFORMANCE_GLITCHED_USER

from .base_page import INVENTORY_URL, BasePage

if TYPE_CHECKING:
    from .inventory_page import InventoryPage

# Textbox names
USERNAME: str = "Username"
PASSWORD: str = "Password"
LOGIN: str = "Login"

# Extra timeouts
INCREASED_TIMEOUT = 20000
SHORT_TIMEOUT = 600

# Labels
CLOSE_ERROR_BUTTON: str = "Close error button"
DOCUMENT_TITLE: str = "Document Title"
LOGO: str = "Logo"
CREDENTIALS = "Credentials Container"
PASSWORD: str = "Password"


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page=page, timeout=timeout)
        self._logo_heading: Locator = self._page.locator(".login_logo")
        self._usernames_heading: Locator = self._page.get_by_role(
            "heading", name="Accepted usernames are:"
        )
        self._password_heading: Locator = self._page.get_by_role(
            "heading", name="Password for all users:"
        )

        self._username: Locator = self._page.get_by_role("textbox", name=USERNAME)
        self._password: Locator = self._page.get_by_role("textbox", name=PASSWORD)
        self._login_button: Locator = self._page.get_by_role("button", name=LOGIN)

        self._error_header: Locator = self._page.locator('[data-test="error"]')
        self._close_error_button: Locator = self._page.locator(
            '[data-test="error-button"]'
        )
        self._usernames_container: Locator = self._page.locator("#login_credentials")
        self._passwords_container: Locator = self._page.locator(".login_password")

    def login(
        self, username: str, password: str, timeout: Optional[int] = None
    ) -> "InventoryPage":  # keep as a string to avoid runtime evaluation
        timeout_ms: int = self._timeout_ms(timeout)

        if username == PERFORMANCE_GLITCHED_USER:
            timeout_ms = INCREASED_TIMEOUT

        self._username.fill(username)
        self._password.fill(password)
        self._login_button.click()

        if self._is_item_displayed(self._error_header, SHORT_TIMEOUT):
            quick_error_message: str = self.get_error_text() or "Unknown login error"
            raise RuntimeError(quick_error_message)

        try:
            self.wait_for_url(INVENTORY_URL, timeout=timeout_ms)
            from .inventory_page import InventoryPage

            return InventoryPage(self._page)
        except RuntimeError:
            error_message = self.get_error_text()
            if error_message:
                raise RuntimeError(error_message)
            raise RuntimeError(
                f"Timed out waiting for login to reach {INVENTORY_URL} after {timeout_ms} ms"
            )

    def is_error_displayed(self, timeout: Optional[int] = None) -> bool:
        if timeout is None:
            return self._error_header.is_visible()
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._error_header, timeout_ms)

    def get_error_text(self) -> str | None:
        if self._is_item_displayed(self._error_header):
            return self._error_header.inner_text().strip()
        else:
            return None

    def dismiss_error(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_element(self._close_error_button, CLOSE_ERROR_BUTTON, timeout_ms)
        try:
            self._close_error_button.click()
            self._error_header.wait_for(state="hidden", timeout=timeout_ms)
            return None
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for error to dismiss (after {timeout_ms} ms)"
            )

    def get_document_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_element(self._logo_heading, DOCUMENT_TITLE, timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self.get_element(self._logo_heading, LOGO, timeout_ms)
        return self._logo_heading.inner_text().strip()

    def is_username_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._username, timeout_ms)

    def is_password_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._password, timeout_ms)

    def is_login_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._login_button, timeout_ms)

    def is_usernames_heading_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._usernames_heading, timeout_ms)

    def get_usernames(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        usernames_container: Locator = self.get_element(
            self._usernames_container, CREDENTIALS, timeout_ms
        )
        text: str = usernames_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("accepted usernames"):
            return lines[1:]
        return lines

    def is_password_heading_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        return self._is_item_displayed(self._password_heading, timeout_ms)

    def get_password(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        password_container: Locator = self.get_element(
            self._passwords_container, CREDENTIALS, timeout_ms
        )
        text: str = password_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("password"):
            password = lines[1:]
        else:
            password: list[str] = lines
        return password[0]

    def is_password_masked(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        password: Locator = self.get_element(self._password, PASSWORD, timeout_ms)
        field_type: str | None = password.get_attribute("type")
        return field_type == "password"

    def attempt_access_unauthenticated(
        self, url: str, timeout: Optional[int] = None
    ) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        self._page.goto(url)
        try:
            self._error_header.wait_for(state="visible", timeout=timeout_ms)
            error_message: str | None = self.get_error_text()
            raise RuntimeError(error_message)
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"No error displayed after accessing {url} without authenticating."
            )
