# fmt: off
from typing import List
from urllib.parse import urljoin

import pytest
from playwright.sync_api import APIResponse, Locator, expect

from data.global_data import ITEM_INDEX
from data.inventory_data import (A_TO_Z,
                                 ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN,
                                 DEFAULT_FILTER_VALUE, DOCUMENT_TITLE,
                                 FILTER_ARGS, FILTER_OPTIONS, FILTER_VALUES,
                                 INVENTORY_ITEMS_DATA, LEFT_MENU_ITEMS,
                                 LOGO_TEXT, ONE, PRODUCTS_TITLE, Z_TO_A,
                                 SortKey)
from data.routes import INVENTORY, ROOT
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

# fmt: on


def assert_images(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.item.image).to_have_count(len(INVENTORY_ITEMS_DATA))
    images: list[Locator] = empty_inventory_page.item.image.all()
    for image in images:
        expect(image).to_be_visible()
        expect(image).to_have_js_property("complete", True)
        expect(image).not_to_have_js_property("naturalWidth", 0)
        source: str | None = image.get_attribute("src")
        # TODO: Investigate replacing this Python assert with a Playwright attribute assertion
        assert source
        image_url: str = urljoin(empty_inventory_page.page.url, source)
        response: APIResponse = empty_inventory_page.page.request.get(image_url)
        expect(response).to_be_ok()


def test_verify_document_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.page).to_have_title(DOCUMENT_TITLE)


def test_verify_inventory_url(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.page).to_have_url(INVENTORY)


def test_verify_page_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.inventory_logo).to_have_text(LOGO_TEXT)


def test_verify_left_menu_components(empty_inventory_page: InventoryPage) -> None:
    empty_inventory_page.menu.hamburger_button.click()
    expect(empty_inventory_page.menu.panel).to_be_visible()
    expect(empty_inventory_page.menu.item).to_have_text(LEFT_MENU_ITEMS)


def test_verify_products_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.products_title).to_have_text(PRODUCTS_TITLE)


def test_verify_default_product_filter_option(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.selected_filter_option).to_have_text(
        DEFAULT_FILTER_VALUE
    )


def test_verify_all_product_filter_options(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.all_filter_options).to_have_text(FILTER_OPTIONS)


# TODO: This test case should include add/remove buttons to consistently test the whole item object
@pytest.mark.parametrize(
    FILTER_ARGS,
    argvalues=FILTER_VALUES,
    ids=[filter_value[0] for filter_value in FILTER_VALUES],
)
def test_verify_products_and_images_after_selecting_filter(
    empty_inventory_page: InventoryPage,
    filter_option: str,
    sort_key: SortKey,
    reverse: bool,
) -> None:
    assert_images(empty_inventory_page)
    # A_TO_Z is the default option, so first we need a change in order to verify
    if filter_option == A_TO_Z:
        empty_inventory_page.set_products_filter(Z_TO_A)
    empty_inventory_page.set_products_filter(filter_option)

    ordered_items: list[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=sort_key, reverse=reverse
    )

    ordered_names: list[str] = [name for name, _ in ordered_items]
    expect(empty_inventory_page.item.name).to_have_text(ordered_names)

    ordered_descriptions: list[str] = [
        details["description"] for _, details in ordered_items
    ]
    expect(empty_inventory_page.item.description).to_have_text(ordered_descriptions)

    ordered_prices: list[str] = [details["price"] for _, details in ordered_items]
    expect(empty_inventory_page.item.price).to_have_text(ordered_prices)

    assert_images(empty_inventory_page)
    images: Locator = empty_inventory_page.item.image
    expected_image_names: List[str] = [name for name, _ in ordered_items]
    for index, expected_name in enumerate(expected_image_names):
        expect(images.nth(index)).to_have_attribute("alt", expected_name)


@pytest.mark.anonymous
def test_verify_error_when_trying_to_access_inventory_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.page.goto(INVENTORY)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN
    )
    expect(login_page.page).to_have_url(ROOT)


def test_verify_items_images_are_displayed(empty_inventory_page: InventoryPage) -> None:
    item_images: Locator = empty_inventory_page.item.image
    expect(item_images).to_have_count(len(INVENTORY_ITEMS_DATA))
    for index in range(len(INVENTORY_ITEMS_DATA)):
        expect(item_images.nth(index)).to_be_visible()


def test_verify_user_can_add_item_to_cart(
    empty_inventory_page: InventoryPage,
) -> None:
    empty_inventory_page.item.add(ITEM_INDEX)
    expect(empty_inventory_page.cart.counter).to_have_text(ONE)


def test_verify_cart_is_empty_by_default(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.cart.counter).to_be_hidden()


def test_verify_cart_is_empty_after_adding_item_and_removing_it(
    empty_inventory_page: InventoryPage,
) -> None:
    empty_inventory_page.item.add(ITEM_INDEX)
    expect(empty_inventory_page.cart.counter).to_have_text(ONE)
    empty_inventory_page.item.remove(ITEM_INDEX)
    expect(empty_inventory_page.cart.counter).to_be_hidden()


def test_go_back_to_continue_shopping(cart_page_with_item: CartPage) -> None:
    inventory_page: InventoryPage = cart_page_with_item.get_inventory_page()
    expect(inventory_page.cart.counter).to_have_text(ONE)


def test_verify_item_remain_in_cart_after_pressing_cancel_in_checkout_step_one_page(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_page_with_item.cancel()
    inventory_page: InventoryPage = cart_page.get_inventory_page()
    expect(inventory_page.cart.counter).to_have_text(ONE)


def test_verify_left_menu_is_closed(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.menu.panel).to_be_hidden()

    empty_inventory_page.menu.hamburger_button.click()
    expect(empty_inventory_page.menu.panel).to_be_visible()

    empty_inventory_page.menu.close_button.click()
    expect(empty_inventory_page.menu.panel).to_be_hidden()
