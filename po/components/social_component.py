from playwright.sync_api import Locator, Page

from po.components.base_component import BaseComponent


class SocialFooter(BaseComponent):
    def __init__(self, page: Page, timeout: int = 10000) -> None:
        super().__init__(page, timeout)
        self.root: Locator = self.locator(".footer")
        self.x: Locator = self.root.get_by_role("link", name="X")
        self.facebook: Locator = self.root.get_by_role("link", name="Facebook")
        self.linkedin: Locator = self.root.get_by_role("link", name="LinkedIn")
        self.copy: Locator = self.root.locator(".footer_copy")
