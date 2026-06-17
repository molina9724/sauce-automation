import random
from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage
from .inventory_page import INVENTORY_URL, InventoryPage

UNLOCKED_USERS = (
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
)
PASSWORD = "secret_sauce"
SUCCESS_LOGIN_DATA = [(user, PASSWORD, INVENTORY_URL) for user in UNLOCKED_USERS]

LOCKED_USERS = ("locked_out_user",)
PERFORMANCE_GLITCHED_USER = "performance_glitch_user"

WRONG_PASSWORD = "wrong_password"

INCREASED_TIMEOUT = 20000
SHORT_TIMEOUT = 600

ALL_USERS = (UNLOCKED_USERS[0],) + LOCKED_USERS + UNLOCKED_USERS[1:]

EXPECTED_LOGIN_USERNAMES = list(ALL_USERS)

RANDOM_UNBLOCKED_USER = random.choice(UNLOCKED_USERS)
RANDOM_LOCKED_USER = random.choice(LOCKED_USERS)


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

    # NOTE: timeout handling is centralized on BasePage._timeout_ms(timeout).
    # Keep helpers like this on the page object rather than using pytest fixtures
    # inside page classes.

    def login(
        self, username: str, password: str, timeout: Optional[int] = None
    ) -> InventoryPage:
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
            return InventoryPage(self._page)
        except PlaywrightTimeoutError:
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
        try:
            self._close_error_button.is_visible()
            self._close_error_button.click()
            self._error_header.wait_for(state="hidden", timeout=timeout_ms)
            return None
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for error to dismiss (after {timeout_ms} ms)"
            )

    def get_document_title(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._logo_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._page.title().strip()

    def get_logo_text(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        self._logo_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._logo_heading.inner_text().strip()

    def is_username_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._username.wait_for(state="visible", timeout=timeout_ms)
        return self._username.is_visible()

    def is_password_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._password.wait_for(state="visible", timeout=timeout_ms)
        return self._password.is_visible()

    def is_login_button_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._login_button.wait_for(state="visible", timeout=timeout_ms)
        return self._login_button.is_visible()

    def is_usernames_heading_visible(self, timeout: Optional[int] = None) -> bool:
        timeout_ms: int = self._timeout_ms(timeout)
        self._usernames_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._usernames_heading.is_visible()

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
        self._usernames_heading.wait_for(state="visible", timeout=timeout_ms)
        return self._usernames_heading.is_visible()

    def get_password(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms = self._timeout_ms(timeout)
        self._credentials_container.wait_for(state="visible", timeout=timeout_ms)
        container: Locator = self._password_container
        text: str = container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("password"):
            password = lines[1:]
        else:
            password: list[str] = lines
        return password
