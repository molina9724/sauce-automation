from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from sauce_project.data.login_data import PERFORMANCE_GLITCHED_USER

from .base_page import INVENTORY_URL, BasePage

if TYPE_CHECKING:
    from .inventory_page import InventoryPage

INCREASED_TIMEOUT = 20000
SHORT_TIMEOUT = 600


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page=page, timeout=timeout)
        self._logo_heading: Locator = self.locator(".login_logo")
        self._usernames_heading: Locator = page.get_by_role(
            "heading", name="Accepted usernames are:"
        )
        self._password_heading: Locator = page.get_by_role(
            "heading", name="Password for all users:"
        )

        self._username: Locator = page.get_by_role("textbox", name="Username")
        self._password: Locator = page.get_by_role("textbox", name="Password")
        self._login_button: Locator = page.get_by_role("button", name="Login")

        self._error_header: Locator = self.locator('[data-test="error"]')
        self._close_error_button: Locator = self.locator('[data-test="error-button"]')
        self._credentials_container: Locator = self.locator("#login_credentials")
        self._password_container: Locator = self.locator(".login_password")

    def login(
        self, username: str, password: str, timeout: Optional[int] = None
    ) -> "InventoryPage":  # keep as a string to avoid runtime evaluation
        timeout_ms: int = self._timeout_ms(timeout)

        if username == PERFORMANCE_GLITCHED_USER:
            timeout_ms = INCREASED_TIMEOUT

        self._username.fill(username)
        self._password.fill(password)
        self._login_button.click()

        try:
            self._error_header.wait_for(state="visible", timeout=SHORT_TIMEOUT)
            error_message = self.get_error_text() or "Unknown login error"
            raise RuntimeError(error_message)
        except PlaywrightTimeoutError:
            pass

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

    def get_error_text(self) -> str | None:
        if self._error_header.is_visible():
            return self._error_header.inner_text().strip()
        else:
            return None

    def is_error_displayed(self, timeout: Optional[int] = None) -> bool:
        if timeout is None:
            return self._error_header.is_visible()
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._error_header.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def dismiss_error(self, timeout: Optional[int] = None) -> None:
        timeout_ms: int = self._timeout_ms(timeout)
        if self._close_error_button.is_visible():
            try:
                self._close_error_button.click()
                self._error_header.wait_for(state="hidden", timeout=timeout_ms)
                return None
            except PlaywrightTimeoutError:
                raise RuntimeError(
                    f"Timed out waiting for error to dismiss (after {timeout_ms} ms)"
                )
        else:
            raise RuntimeError(
                f"Close error button was not displayed (after {timeout_ms} ms)"
            )

    def get_document_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._logo_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._logo_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._logo_heading.inner_text().strip()

    def is_username_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._username.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_password_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._password.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_login_button_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._login_button.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def is_usernames_heading_displayed(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._usernames_heading.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_credentials_container_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._credentials_container.wait_for(state="visible", timeout=timeout_ms)
        return self._credentials_container.inner_text()

    def get_usernames(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        self._credentials_container.wait_for(state="visible", timeout=timeout_ms)
        text: str = self._credentials_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("accepted usernames"):
            return lines[1:]
        return lines

    def is_password_usernames_heading_displayed(
        self, timeout: Optional[int] = None
    ) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        try:
            self._password_heading.wait_for(state="visible", timeout=timeout_ms)
            return True
        except PlaywrightTimeoutError:
            return False

    def get_password(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        self._credentials_container.wait_for(state="visible", timeout=timeout_ms)
        container: Locator = self._password_container
        text: str = container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("password"):
            password = lines[1:]
        else:
            password: list[str] = lines
        return password

    def is_password_masked(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        if self.is_password_displayed(timeout_ms):
            password_masked: str | None = self._password.get_attribute("type")
            if password_masked == "password":
                return True
        return False

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
                f"No error displayed after accessing {INVENTORY_URL} without authenticating."
            )
