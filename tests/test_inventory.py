# fmt: off
from typing import List

import pytest
from playwright.sync_api import expect

from data.global_data import ITEM_INDEX
from data.inventory_data import (ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN,
                                 DEFAULT_FILTER_VALUE, DOCUMENT_TITLE,
                                 FILTER_OPTIONS, HIGH_TO_LOW,
                                 INVENTORY_ITEMS_DATA, LEFT_MENU_ITEMS,
                                 LOW_TO_HIGH, PRODUCTS_TITLE, Z_TO_A,
                                 get_price_value)
from po.pages.base_page import INVENTORY_URL
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

# fmt: on


def test_verify_inventory_url(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.page).to_have_url(INVENTORY_URL)


def test_verify_page_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.inventory_logo).to_have_text(DOCUMENT_TITLE)


def test_verify_left_menu_components(empty_inventory_page: InventoryPage) -> None:
    empty_inventory_page.menu.open()
    expect(empty_inventory_page.menu.left_menu).to_be_visible()
    left_menu_items: List[str] = empty_inventory_page.menu.get_left_menu_elements()
    assert left_menu_items == LEFT_MENU_ITEMS


def test_verify_products_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.products_title).to_have_text(PRODUCTS_TITLE)


def test_verify_default_product_filter_options(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.selected_filter_option).to_have_text(
        DEFAULT_FILTER_VALUE
    )


def test_verify_all_product_filter_options(
    empty_inventory_page: InventoryPage,
) -> None:
    assert empty_inventory_page.get_products_filter_options() == FILTER_OPTIONS


def test_verify_z_to_a_filter(empty_inventory_page: InventoryPage) -> None:
    empty_inventory_page.set_products_filter(Z_TO_A)
    z_to_a_ordered_results: dict[str, dict[str, str]] = (
        empty_inventory_page.get_all_products_information()
    )

    actual: List[tuple[str, dict[str, str]]] = list(z_to_a_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), reverse=True
    )
    assert actual == expected


def test_verify_low_to_high_filter(empty_inventory_page: InventoryPage) -> None:
    empty_inventory_page.set_products_filter(LOW_TO_HIGH)
    low_to_high_ordered_results: dict[str, dict[str, str]] = (
        empty_inventory_page.get_all_products_information()
    )

    actual: List[tuple[str, dict[str, str]]] = list(low_to_high_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=get_price_value
    )
    assert actual == expected


def test_verify_high_to_low_filter(empty_inventory_page: InventoryPage) -> None:
    empty_inventory_page.set_products_filter(HIGH_TO_LOW)
    high_to_low_ordered_results: dict[str, dict[str, str]] = (
        empty_inventory_page.get_all_products_information()
    )

    actual: List[tuple[str, dict[str, str]]] = list(high_to_low_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=get_price_value, reverse=True
    )
    assert actual == expected


@pytest.mark.anonymous
def test_verify_error_when_trying_to_access_inventory_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.goto(INVENTORY_URL)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN
    )


def test_verify_items_images_are_displayed(
    empty_inventory_page: InventoryPage,
) -> None:
    assert empty_inventory_page.are_items_images_displayed()


def test_verify_user_can_add_item_to_cart(
    empty_inventory_page: InventoryPage,
) -> None:
    empty_inventory_page.add_item_to_cart(ITEM_INDEX)
    assert empty_inventory_page.cart.get_cart_counter() == 1


def test_verify_cart_is_empty_by_default(
    empty_inventory_page: InventoryPage,
) -> None:
    assert empty_inventory_page.cart.is_cart_empty()


def test_verify_cart_is_empty_after_adding_item_and_removing_it(
    empty_inventory_page: InventoryPage,
) -> None:
    empty_inventory_page.add_item_to_cart(ITEM_INDEX)
    assert empty_inventory_page.cart.get_cart_counter() == 1
    empty_inventory_page.remove_item_from_cart(ITEM_INDEX)
    assert empty_inventory_page.cart.is_cart_empty()


def test_go_back_to_continue_shopping(cart_page_with_item: CartPage) -> None:
    inventory_page: InventoryPage = cart_page_with_item.get_inventory_page()
    assert inventory_page.cart.get_cart_counter() == 1


def test_verify_item_remain_in_cart_after_pressing_cancel_in_checkout_step_one_page(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_with_item.cart.get_cart_page()
    inventory_page: InventoryPage = cart_page.get_inventory_page()
    assert inventory_page.cart.get_cart_counter() == 1


def test_verify_left_menu_is_closed(
    empty_inventory_page: InventoryPage,
) -> None:
    assert empty_inventory_page.menu.is_left_menu_hidden()

    empty_inventory_page.menu.open()
    assert empty_inventory_page.menu.is_left_menu_displayed()

    empty_inventory_page.menu.close()
    assert empty_inventory_page.menu.is_left_menu_hidden()
