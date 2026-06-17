import pytest
from playwright.sync_api import Page

from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


@pytest.fixture(scope="function", autouse=True)
def login(page: Page) -> InventoryPage:
    page.goto(BASE_URL)
    inventory_page: InventoryPage = LoginPage(page).login(
        username="standard_user", password="secret_sauce"
    )
    return inventory_page


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


def test_01_verify__inventory_url(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_url() == "https://www.saucedemo.com/inventory.html"
