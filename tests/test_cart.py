from playwright.sync_api import expect

from sauce_project.po.pages.cart_page import CartPage


def test_00_verify__cart_url(cart_page: CartPage) -> None:
    expect(cart_page._page).to_have_url("https://www.saucedemo.com/cart.html")
