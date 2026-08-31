# fmt: off
from typing import TYPE_CHECKING

from playwright.sync_api import Locator, Page

from data.login_data import PERFORMANCE_GLITCHED_USER
from data.routes import INVENTORY

from ..components.form_validation import FormValidation
from .base_page import BasePage

if TYPE_CHECKING:
    from .inventory_page import InventoryPage
# fmt: on

INCREASED_TIMEOUT: int = 20000


class LoginPage(BasePage):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page=page, timeout=timeout)
        self.logo_heading: Locator = self.page.locator(".login_logo")
        self.usernames_heading: Locator = self.page.get_by_role(
            "heading", name="Accepted usernames are:"
        )
        self.password_heading: Locator = self.page.get_by_role(
            "heading", name="Password for all users:"
        )

        self.form_validation = FormValidation(self.page)

        self.username: Locator = self.page.get_by_role("textbox", name="Username")
        self.password: Locator = self.page.get_by_role("textbox", name="Password")
        self.login_button: Locator = self.page.get_by_role("button", name="Login")
        self.close_error_button: Locator = self.page.locator(
            ".error-message-container.error .error-button"
        )

        self.usernames_container: Locator = self.page.locator("#login_credentials")
        self.passwords_container: Locator = self.page.locator(".login_password")

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
        self.page.wait_for_url(INVENTORY, timeout=timeout)

        from .inventory_page import InventoryPage

        return InventoryPage(self.page)

    def dismiss_error(self) -> None:
        self.close_error_button.click()
        self.form_validation.error_heading.wait_for(state="hidden")

    def get_usernames(self) -> list[str]:
        usernames_container: Locator = self.usernames_container
        text: str = usernames_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]
        if lines and lines[0].lower().startswith("accepted usernames"):
            return lines[1:]
        return lines

    def get_password(self) -> str:
        password_container: Locator = self.passwords_container
        text: str = password_container.inner_text()
        lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]
        if lines and lines[0].lower().startswith("password"):
            password = lines[1:]
        else:
            password: list[str] = lines
        return password[0]
