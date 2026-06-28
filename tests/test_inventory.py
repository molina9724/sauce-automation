from typing import List

import pytest
from playwright.sync_api import expect

from sauce_project.data.products import (
    ALL_PRICES_FILTER_OPTIONS,
    DEFAULT_FILTER_VALUE,
    INVENTORY_ITEMS_DATA,
    ITEM_INDEX,
    LEFT_MENU_COMPONENTS,
)
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


def get_price_value(item: tuple[str, dict[str, str]]) -> float:
    _, data = item
    price_text: str = data["price"]
    return float(price_text[1:])


def test_00_verify__inventory_url(inventory_page: InventoryPage) -> None:
    expect(inventory_page._page).to_have_url("https://www.saucedemo.com/inventory.html")


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


def test_07_verify_z_to_a_filter(inventory_page: InventoryPage) -> None:
    inventory_page.set_products_filter("Name (Z to A)")
    z_to_a_ordered_results: dict[str, dict[str, str]] = (
        inventory_page.get_all_products_information()
    )

    actual: List[tuple[str, dict[str, str]]] = list(z_to_a_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), reverse=True
    )
    assert actual == expected


def test_08_verify_low_to_high_filter(inventory_page: InventoryPage) -> None:
    inventory_page.set_products_filter("Price (low to high)")
    low_to_high_ordered_results = inventory_page.get_all_products_information()

    actual: List[tuple[str, dict[str, str]]] = list(low_to_high_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=get_price_value
    )
    assert actual == expected


def test_09_high_to_low_filter(inventory_page: InventoryPage):
    inventory_page.set_products_filter("Price (high to low)")
    high_to_low_ordered_results: dict[str, dict[str, str]] = (
        inventory_page.get_all_products_information()
    )

    actual: List[tuple[str, dict[str, str]]] = list(high_to_low_ordered_results.items())
    expected: List[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=get_price_value, reverse=True
    )
    assert actual == expected


def test_10_verify_exception_when_trying_to_access_inventory_page_without_login(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.attempt_access_unauthenticated()
    assert (
        "Epic sadface: You can only access '/inventory.html' when you are logged in."
        == str(exception_information.value)
    )


def test_11_verify_items_images_are_displayed(inventory_page: InventoryPage) -> None:
    assert inventory_page.are_items_images_displayed()


def test_12_verify_user_can_add_item_to_cart(inventory_page: InventoryPage) -> None:
    inventory_page.add_item_to_cart(ITEM_INDEX)
    assert inventory_page.get_cart_counter() == 1


def test_13_verify_cart_is_empty_by_default(inventory_page: InventoryPage) -> None:
    assert inventory_page.is_cart_empty()


def test_14_verify_cart_is_empty_after_adding_item_and_removing_it(
    inventory_page: InventoryPage,
) -> None:
    inventory_page.add_item_to_cart(ITEM_INDEX)
    assert inventory_page.get_cart_counter() == 1
    inventory_page.remove_item_from_cart(ITEM_INDEX)
    assert inventory_page.is_cart_empty()


def test_15_go_back_to_continue_shopping(cart_page_with_item: CartPage) -> None:
    inventory_page: InventoryPage = cart_page_with_item.get_inventory_page()
    assert inventory_page.get_cart_counter() == 1
