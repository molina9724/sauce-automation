# fmt: off

import pytest
from playwright.sync_api import Locator, expect

from data.inventory_data import (A_TO_Z,
                                 ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN,
                                 ALL_ITEMS_INDEX, DEFAULT_FILTER_VALUE,
                                 DOCUMENT_TITLE, FILTER_ARGS, FILTER_OPTIONS,
                                 FILTER_VALUES, INDEX, LOGO_TEXT,
                                 PRODUCT_DETAIL_ARGS, PRODUCT_DETAIL_DATA,
                                 PRODUCT_DETAIL_IDS, PRODUCTS_TITLE, Z_TO_A,
                                 ZERO, SortKey)
from data.item_data import (ADD_TO_CART, INVENTORY_ITEMS_DATA, ITEM_INDEX, ONE,
                            REMOVE)
from data.routes import CART, INVENTORY, INVENTORY_ITEM, ROOT
from po.pages.cart_page import CartPage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_item_page import InventoryItemPage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage
from tests.test_image import general_image_assert

# fmt: on


def assert_item_images(inventory_page: InventoryPage) -> None:
    expect(inventory_page.item.image).to_have_count(len(INVENTORY_ITEMS_DATA))
    images: list[Locator] = inventory_page.item.image.all()
    for image in images:
        general_image_assert(inventory_page, image)


def verify_item_can_be_added(
    inventory_page: InventoryPage, index: int, expected_count: int
) -> None:
    expect(inventory_page.item.button.nth(index)).to_have_text(ADD_TO_CART)

    inventory_page.item.add(index)

    expect(inventory_page.cart.counter).to_have_text(str(expected_count))
    expect(inventory_page.item.button.nth(index)).to_have_text(REMOVE)


def verify_item_can_be_removed(
    inventory_page: InventoryPage, index: int, expected_count: int
) -> None:
    expect(inventory_page.item.button.nth(index)).to_have_text(REMOVE)

    inventory_page.item.remove(index)

    if expected_count == 0:
        expect(inventory_page.cart.counter).to_be_hidden()
    else:
        expect(inventory_page.cart.counter).to_have_text(str(expected_count))
    expect(inventory_page.item.button.nth(index)).to_have_text(ADD_TO_CART)


def test_verify_document_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.page).to_have_title(DOCUMENT_TITLE)


def test_verify_inventory_url(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.page).to_have_url(INVENTORY)


def test_verify_page_title(empty_inventory_page: InventoryPage) -> None:
    expect(empty_inventory_page.inventory_logo).to_have_text(LOGO_TEXT)


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


@pytest.mark.parametrize(
    FILTER_ARGS,
    argvalues=FILTER_VALUES,
    ids=[filter_value[0] for filter_value in FILTER_VALUES],
)
def test_verify_products_information_after_selecting_filter(
    inventory_page_with_item: InventoryPage,
    filter_option: str,
    sort_key: SortKey,
    reverse: bool,
) -> None:
    assert_item_images(inventory_page_with_item)
    # A_TO_Z is the default option, so first we need a change in order to verify
    if filter_option == A_TO_Z:
        inventory_page_with_item.set_products_filter(Z_TO_A)
    inventory_page_with_item.set_products_filter(filter_option)

    ordered_items: list[tuple[str, dict[str, str]]] = sorted(
        INVENTORY_ITEMS_DATA.items(), key=sort_key, reverse=reverse
    )

    ordered_names: list[str] = [name for name, _ in ordered_items]
    expect(inventory_page_with_item.item.name).to_have_text(ordered_names)

    ordered_descriptions: list[str] = [
        details["description"] for _, details in ordered_items
    ]
    expect(inventory_page_with_item.item.description).to_have_text(ordered_descriptions)

    ordered_prices: list[str] = [details["price"] for _, details in ordered_items]
    expect(inventory_page_with_item.item.price).to_have_text(ordered_prices)

    assert_item_images(inventory_page_with_item)
    images: Locator = inventory_page_with_item.item.image
    expected_image_names: list[str] = [name for name, _ in ordered_items]
    for index, expected_name in enumerate(expected_image_names):
        expect(images.nth(index)).to_have_attribute("alt", expected_name)

    selected_name: str = list(INVENTORY_ITEMS_DATA)[ITEM_INDEX]
    expected_button_labels: list[str] = [
        REMOVE if name == selected_name else ADD_TO_CART for name, _ in ordered_items
    ]
    expect(inventory_page_with_item.item.button).to_have_text(expected_button_labels)


@pytest.mark.anonymous
def test_verify_error_when_trying_to_access_inventory_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.page.goto(INVENTORY)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN
    )
    expect(login_page.page).to_have_url(ROOT)


@pytest.mark.parametrize(
    INDEX,
    argvalues=ALL_ITEMS_INDEX,
    ids=PRODUCT_DETAIL_IDS,
)
def test_verify_user_can_add_item_to_cart(
    empty_inventory_page: InventoryPage, index: int
) -> None:
    verify_item_can_be_added(empty_inventory_page, index, ONE)


@pytest.mark.parametrize(
    INDEX,
    argvalues=ALL_ITEMS_INDEX,
    ids=PRODUCT_DETAIL_IDS,
)
def test_verify_user_can_remove_item_after_adding_it(
    empty_inventory_page: InventoryPage, index: int
) -> None:
    verify_item_can_be_added(empty_inventory_page, index, ONE)
    verify_item_can_be_removed(empty_inventory_page, index, ZERO)


def test_verify_user_can_add_all_items_to_cart(
    empty_inventory_page: InventoryPage,
) -> None:
    for index in ALL_ITEMS_INDEX:
        verify_item_can_be_added(empty_inventory_page, index, index + 1)


def test_verify_user_can_remove_all_items_from_cart(
    inventory_page_with_all_items: InventoryPage,
) -> None:
    for index in ALL_ITEMS_INDEX:
        expected_count: int = len(ALL_ITEMS_INDEX) - (index + 1)
        verify_item_can_be_removed(inventory_page_with_all_items, index, expected_count)


def test_verify_cart_is_empty_by_default(
    empty_inventory_page: InventoryPage,
) -> None:
    expect(empty_inventory_page.cart.counter).to_be_hidden()


def test_verify_item_remains_in_cart_after_pressing_continue_shopping_button(
    cart_page_with_item: CartPage,
) -> None:
    inventory_page: InventoryPage = cart_page_with_item.get_inventory_page()
    expect(inventory_page.page).to_have_url(INVENTORY)
    expect(inventory_page.item.button.nth(ITEM_INDEX)).to_have_text(REMOVE)
    expect(inventory_page.cart.counter).to_have_text(str(ONE))


def test_verify_cancel_from_checkout_step_two_preserves_cart_item(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    inventory_page: InventoryPage = checkout_step_2_page_with_item.cancel()
    expect(inventory_page.page).to_have_url(INVENTORY)
    expect(inventory_page.cart.counter).to_have_text(str(ONE))
    expect(inventory_page.item.button.nth(ITEM_INDEX)).to_have_text(REMOVE)


@pytest.mark.parametrize(
    PRODUCT_DETAIL_ARGS,
    argvalues=PRODUCT_DETAIL_DATA,
    ids=PRODUCT_DETAIL_IDS,
)
def test_verify_user_can_open_product_details_from_product_name(
    empty_inventory_page: InventoryPage, index: int, product_id: str
) -> None:
    inventory_page = empty_inventory_page
    product_page: InventoryItemPage = inventory_page.open_item_by_name(index)
    expect(product_page.page).to_have_url(f"{INVENTORY_ITEM}{product_id}")
    inventory_page: InventoryPage = product_page.back_to_products()
    expect(inventory_page.page).to_have_url(INVENTORY)


@pytest.mark.parametrize(
    PRODUCT_DETAIL_ARGS,
    argvalues=PRODUCT_DETAIL_DATA,
    ids=PRODUCT_DETAIL_IDS,
)
def test_verify_user_can_open_product_details_from_product_image(
    empty_inventory_page: InventoryPage, index: int, product_id: str
) -> None:
    inventory_page = empty_inventory_page
    product_page: InventoryItemPage = inventory_page.open_item_by_image(index)
    expect(product_page.page).to_have_url(f"{INVENTORY_ITEM}{product_id}")
    inventory_page: InventoryPage = product_page.back_to_products()
    expect(inventory_page.page).to_have_url(INVENTORY)


def test_verify_user_can_navigate_to_cart_from_inventory_page(
    empty_inventory_page: InventoryPage,
) -> None:
    cart_page: CartPage = empty_inventory_page.cart.get_cart_page()
    expect(cart_page.page).to_have_url(CART)
