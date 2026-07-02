from playwright.sync_api import expect

from sauce_project.data.cart_data import CART_ITEM_DATA
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.checkout_step_1_page import CheckoutStepOnePage


def test_00_verify__cart_url(empty_cart_page: CartPage) -> None:
    expect(empty_cart_page._page).to_have_url("https://www.saucedemo.com/cart.html")


def test_01_cart_is_empty(empty_cart_page: CartPage) -> None:
    assert empty_cart_page.is_cart_empty()


def test_02_correct_item_in_cart(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_all_products_information() == CART_ITEM_DATA


def test_03_item_is_removed(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_amount_of_items_in_cart() == 1
    cart_page_with_item.remove_item(0)
    assert cart_page_with_item.is_cart_empty()


def test_04_several_items_in_cart(cart_page_with_all_items: CartPage) -> None:
    assert cart_page_with_all_items.get_amount_of_items_in_cart() == 6


def test_05_verify_items_remain_in_cart_after_pressing_cancel_in_checkout_step_one_page(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_with_item.get_cart_page()
    assert cart_page.get_all_products_information() == CART_ITEM_DATA
