# fmt: off
import pytest
from playwright.sync_api import expect

from data.cart_data import (ACCESS_CART_PAGE_WITHOUT_LOGIN_ERROR,
                            ALL_ITEMS_INDEX, CART_ITEM_DATA)
from po.pages.base_page import CART_URL
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.login_page import LoginPage

# fmt: on


def test_verify_cart_url(empty_cart_page: CartPage) -> None:
    expect(empty_cart_page.page).to_have_url(CART_URL)


def test_verify_cart_is_empty(empty_cart_page: CartPage) -> None:
    expect(empty_cart_page.cart.counter).to_be_hidden()


def test_verify_correct_item_in_cart(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_all_products_information() == CART_ITEM_DATA


def test_verify_item_is_removed(cart_page_with_item: CartPage) -> None:
    expect(cart_page_with_item.item).to_have_count(1)
    cart_page_with_item.remove_item(0)
    expect(cart_page_with_item.cart.counter).to_be_hidden()
    expect(cart_page_with_item.item).to_have_count(0)


def test_verify_several_items_can_be_added_to_cart(
    cart_page_with_all_items: CartPage,
) -> None:
    expect(cart_page_with_all_items.item).to_have_count(len(ALL_ITEMS_INDEX))


def test_verify_items_remain_in_cart_after_pressing_cancel_in_checkout_step_one_page(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_with_item.cancel()
    assert cart_page.get_all_products_information() == CART_ITEM_DATA


@pytest.mark.anonymous
def test_verify_error_when_accessing_cart_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.goto(CART_URL)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_CART_PAGE_WITHOUT_LOGIN_ERROR
    )
