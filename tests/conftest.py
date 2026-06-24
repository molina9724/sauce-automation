import pytest
from playwright.sync_api import Page

from ..po.pages.base_page import LOGIN_URL
from ..po.pages.cart_page import CartPage
from ..po.pages.inventory_page import InventoryPage
from ..po.pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    page.goto(LOGIN_URL)
    return LoginPage(page)


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    return login_page.login(username="standard_user", password="secret_sauce")


@pytest.fixture
def cart_page(inventory_page: InventoryPage) -> CartPage:
    cart_page: CartPage = inventory_page.get_cart_page()
    return cart_page
