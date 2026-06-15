from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self._logo_heading: Locator = self.locator(".login_logo")
        self._usernames_heading: Locator = self.locator(".login_credentials")
        self._password_heading: Locator = page.get_by_role(
            "heading", name="Password for all users:"
        )

        self._username: Locator = page.get_by_role("textbox", name="Username")
        self._password: Locator = page.get_by_role("textbox", name="Password")
        self._login_button: Locator = page.get_by_role("button", name="Login")

        self._error_header: Locator = self.locator('[data-test="error"]')
        self._error_close_button: Locator = self.locator('[data-test="error-button"]')
        self._credentials_container: Locator = self.locator("#login_credentials")
        self._password_container: Locator = self.locator(".login_password")

        self._hamburger_button: Locator = page.get_by_role("button", name="Open Menu")
        self._logout_link: Locator = page.get_by_role("link", name="Logout")

    def login(
        self, username: str, password: str, timeout: Optional[int] = None
    ) -> None:
        self._username.fill(username)
        self._password.fill(password)
        self._login_button.click()
        return None

    def get_error_text(self) -> str | None:
        if self._error_header.is_visible():
            return self._error_header.inner_text().strip()
        else:
            return None

    def dismiss_error(self, timeout: Optional[int] = None):
        timeout_ms = timeout if timeout is not None else self._timeout
        try:
            self._error_close_button.is_visible()
            self._error_close_button.click()
            self._error_header.wait_for(state="hidden", timeout=timeout_ms)
            return None
        except PlaywrightTimeoutError:
            raise RuntimeError(
                f"Timed out waiting for error to dismiss (after {timeout_ms} ms)"
            )
