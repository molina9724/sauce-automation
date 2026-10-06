from playwright.sync_api import Locator, Page

from po.components.base_component import BaseComponent


class BasePage(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.logo: Locator = self.page.locator(".app_logo, .login_logo")
