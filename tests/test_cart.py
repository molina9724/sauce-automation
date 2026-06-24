import pytest
from playwright.sync_api import Page

from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


@pytest.fixture
def cart_page(page: Page) -> CartPage:
    page.goto(BASE_URL)
    inventory_page: InventoryPage = LoginPage(page).login(
        username="standard_user", password="secret_sauce"
    )
    cart_page: CartPage = inventory_page.get_cart_page()
    return cart_page


def test_00_verify__cart_url(cart_page: CartPage) -> None:
    assert cart_page.get_url() == "https://www.saucedemo.com/cart.html"
