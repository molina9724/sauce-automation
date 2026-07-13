import pytest
from playwright.sync_api import expect

# fmt: off
from sauce_project.data.cart_data import (ACCESS_CART_PAGE_WITHOUT_LOGIN_ERROR,
                                          CART_ITEM_DATA)
# fmt: on
from sauce_project.po.pages.base_page import CART_URL
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.checkout_step_1_page import CheckoutStepOnePage
from sauce_project.po.pages.login_page import LoginPage


def test_00_verify__cart_url(empty_cart_page: CartPage) -> None:
    expect(empty_cart_page._page).to_have_url(CART_URL)


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


def test_06_verify_exception_when_accessing_checkout_step_1_page_error_without_login(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.attempt_access_unauthenticated(CART_URL)
    assert ACCESS_CART_PAGE_WITHOUT_LOGIN_ERROR == str(exception.value)
