import random
from typing import Optional

from playwright.sync_api import Locator, Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from .base_page import BasePage
from .inventory_page import INVENTORY_URL

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
WRONG_PASSWORD = "wrong_password"

ALL_USERS = (UNLOCKED_USERS[0],) + LOCKED_USERS + UNLOCKED_USERS[1:]

EXPECTED_LOGIN_USERNAMES = list(ALL_USERS)

RANDOM_UNBLOCKED_USER = random.choice(UNLOCKED_USERS)
RANDOM_LOCKED_USER = random.choice(LOCKED_USERS)


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
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
        self._error_close_button: Locator = self.locator('[data-test="error-button"]')
        self._credentials_container: Locator = self.locator("#login_credentials")
        self._password_container: Locator = self.locator(".login_password")

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
