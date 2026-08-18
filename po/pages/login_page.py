# fmt: off
from typing import TYPE_CHECKING, Optional

from playwright.sync_api import Locator, Page

from data.login_data import PERFORMANCE_GLITCHED_USER

from ..components.form_validation import FormValidation
from .base_page import INCREASED_TIMEOUT, INVENTORY_URL, BasePage

if TYPE_CHECKING:
    from .inventory_page import InventoryPage
# fmt: on

# Textbox names
USERNAME: str = "Username"
PASSWORD: str = "Password"
LOGIN: str = "Login"

# Labels
CREDENTIALS = "Credentials Container"


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page=page, timeout=timeout)
        self.logo_heading: Locator = self._page.locator(".login_logo")
        self.usernames_heading: Locator = self._page.get_by_role(
            "heading", name="Accepted usernames are:"
        )
        self.password_heading: Locator = self._page.get_by_role(
            "heading", name="Password for all users:"
        )

        self.form_validation = FormValidation(self._page)

        self.username: Locator = self._page.get_by_role("textbox", name=USERNAME)
        self.password: Locator = self._page.get_by_role("textbox", name=PASSWORD)
        self.login_button: Locator = self._page.get_by_role("button", name=LOGIN)
        self.close_error_button: Locator = self._page.locator(
            ".error-message-container.error .error-button"
        )

        self.usernames_container: Locator = self._page.locator("#login_credentials")
        self.passwords_container: Locator = self._page.locator(".login_password")

    def get_fields(self) -> tuple[Locator, Locator]:
        username: Locator = self.username
        password: Locator = self.password

        return username, password

    def get_fields_containers(self) -> tuple[Locator, Locator]:
        username, password = self.get_fields()

        # The error icon is a sibling of the field, not a child of it
        username_parent: Locator = self.get_parent(username)
        password_parent: Locator = self.get_parent(password)

        return username_parent, password_parent

    def submit_credentials(self, username: str, password: str) -> None:
        self.username.fill(username)
        self.password.fill(password)
        self.login_button.click()

    def login(
        self, username: str, password: str
    ) -> "InventoryPage":  # keep as a string to avoid runtime evaluation
        self.submit_credentials(username, password)
        if username == PERFORMANCE_GLITCHED_USER:
            timeout: int = INCREASED_TIMEOUT
        else:
            timeout = self._timeout
        self._page.wait_for_url(INVENTORY_URL, timeout=timeout)

        from .inventory_page import InventoryPage

        return InventoryPage(self._page)

    def dismiss_error(self) -> None:
        self.close_error_button.click()
        self.form_validation.error_heading.wait_for(state="hidden")

    def get_usernames(self, timeout: Optional[int] = None) -> list[str]:
        timeout_ms: int = self._timeout_ms(timeout)
        usernames_container: Locator = self.get_element(
            self.usernames_container, CREDENTIALS, timeout_ms
        )
        text: str = usernames_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("accepted usernames"):
            return lines[1:]
        return lines

    def get_password(self, timeout: Optional[int] = None) -> str:
        timeout_ms: int = self._timeout_ms(timeout)
        password_container: Locator = self.get_element(
            self.passwords_container, CREDENTIALS, timeout_ms
        )
        text: str = password_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

        if lines and lines[0].lower().startswith("password"):
            password = lines[1:]
        else:
            password: list[str] = lines
        return password[0]
