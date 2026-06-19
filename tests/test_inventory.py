from typing import List

import pytest
from playwright.sync_api import Page

from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage

LEFT_MENU_COMPONENTS: List[str] = ["All Items", "About", "Logout", "Reset App State"]
ALL_PRICES_FILTER_OPTIONS: List[str] = [
    "Name (A to Z)",
    "Name (Z to A)",
    "Price (low to high)",
    "Price (high to low)",
]
DEFAULT_FILTER_VALUE = ALL_PRICES_FILTER_OPTIONS[0]

# Sorted by Name (A to Z) by default
INVENTORY_PRODUCTS: dict[str, dict[str, str]] = {
    "Sauce Labs Backpack": {
        "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        "price": "$29.99",
    },
    "Sauce Labs Bike Light": {
        "description": "A red light isn't the caused of traffic jams on the information super highway. And it's not caused by a Problem User either. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        "price": "$9.99",
    },
    "Sauce Labs Bolt T-Shirt": {
        "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From any browser, on any OS, any day of the week. 100% Cotton. Hand wash only.",
        "price": "$15.99",
    },
    "Sauce Labs Fleece Jacket": {
        "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a]]",
        "price": "$49.99",
    },
    "Sauce Labs Onesie": {
        "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        "price": "$7.99",
    },
    "Test.allTheThings() T-Shirt (Red)": {
        "description": "This classic Sauce Labs t-shirt is perfect to wear when cashing in an ideation session. Code!",
        "price": "$15.99",
    },
}


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


def test_01_verify_document_title(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_document_title() == "Swag Labs"


def test_02_verify_page_title(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_logo_text() == "Swag Labs"


def test_03_verify_left_menu_components(inventory_page: InventoryPage) -> None:
    inventory_page.open_hamburger_button()
    assert inventory_page.is_left_menu_displayed()
    left_menu_items = inventory_page.get_left_menu_elements()
    assert left_menu_items == LEFT_MENU_COMPONENTS


def test_04_verify_products_title(inventory_page: InventoryPage) -> None:
    assert inventory_page.get_products_title() == "Products"


def test_05_verify_default_product_filter_options(
    inventory_page: InventoryPage,
) -> None:
    assert inventory_page.get_products_filter_selected_option() == DEFAULT_FILTER_VALUE


def test_06_verify_all_product_filter_options(
    inventory_page: InventoryPage,
) -> None:
    assert inventory_page.get_products_filter_options() == ALL_PRICES_FILTER_OPTIONS
