import pytest
from playwright.sync_api import Locator, Page, expect

from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage

LEFT_MENU_COMPONENTS = ["All Items", "About", "Logout", "Reset App State"]


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


def test_00_verify__inventory_url(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_url() == "https://www.saucedemo.com/inventory.html"


def test_01_document_title(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_document_title() == "Swag Labs"


def test_02_page_title(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_logo_text() == "Swag Labs"


def test_03_left_menu_components(inventory_page: InventoryPage) -> None:
    inventory_page.open_hamburger_button()
    assert inventory_page.is_left_menu_displayed()
    left_menu_items = inventory_page.get_left_menu_elements()
    assert left_menu_items == LEFT_MENU_COMPONENTS
