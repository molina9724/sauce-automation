import pytest
from _pytest.mark.structures import ParameterSet

from data.access_without_login_data import get_error
from data.cart_data import CART_ITEM_DATA, CART_ITEMS_DATA
from data.inventory_data import PRODUCT_DETAIL_DATA
from data.routes import (
    CART,
    CHECKOUT_COMPLETE,
    CHECKOUT_STEP_1,
    CHECKOUT_STEP_2,
    INVENTORY,
    INVENTORY_ITEM,
)

PAGE_FIXTURE: str = "page_fixture"

FIXTURES_WITH_EMPTY_CART: list[str] = [
    "empty_inventory_page",
    "inventory_item_page",
    "empty_cart_page",
    "empty_checkout_step_1_page",
    "empty_checkout_step_2_page",
    "checkout_complete_page",
]
FIXTURES_WITH_ITEM_IN_CART: list[str] = [
    "inventory_page_with_item",
    "inventory_item_page_with_item",
    "cart_page_with_item",
    "checkout_step_1_page_with_item",
    "checkout_step_2_page_with_item",
]
FIXTURES_WITH_AND_WITHOUT_ITEMS: list[str] = (
    FIXTURES_WITH_EMPTY_CART + FIXTURES_WITH_ITEM_IN_CART
)

GLOBAL_PAGE_FIXTURES: list[ParameterSet] = [
    pytest.param("login_page", marks=pytest.mark.anonymous, id="login_page"),
    *[pytest.param(fixture, id=fixture) for fixture in FIXTURES_WITH_EMPTY_CART],
]

MENU_PAGE_FIXTURES: list[ParameterSet] = [
    pytest.param("empty_inventory_page", False, id="empty_inventory_page"),
    pytest.param("inventory_item_page", False, id="inventory_item_page"),
    pytest.param(
        "inventory_item_page_with_item", True, id="inventory_item_page_with_item"
    ),
    pytest.param("empty_cart_page", False, id="empty_cart_page"),
    pytest.param(
        "empty_checkout_step_1_page",
        False,
        id="empty_checkout_step_1_page",
    ),
    pytest.param(
        "empty_checkout_step_2_page",
        False,
        id="empty_checkout_step_2_page",
    ),
    pytest.param("inventory_page_with_item", True, id="inventory_page_with_item"),
    pytest.param("cart_page_with_item", True, id="cart_page_with_item"),
    pytest.param(
        "checkout_step_1_page_with_item",
        True,
        id="checkout_step_1_page_with_item",
    ),
    pytest.param(
        "checkout_step_2_page_with_item",
        True,
        id="checkout_step_2_page_with_item",
    ),
    pytest.param(
        "checkout_complete_page",
        False,
        id="checkout_complete_page_after_purchase",
    ),
]

CART_LIST_FIXTURES: list[str] = [
    "cart_page_with_all_items",
    "checkout_step_2_page_with_all_items",
]

CHECKOUT_STEP_2_ORDER_ARGS: str = "page_fixture, items"
CHECKOUT_STEP_2_VALUES: list[ParameterSet] = [
    pytest.param(
        "checkout_step_2_page_with_item",
        CART_ITEM_DATA,
        id="single_item",
    ),
    pytest.param(
        "checkout_step_2_page_with_all_items",
        CART_ITEMS_DATA,
        id="all_items",
    ),
]

ACCESS_WITHOUT_LOGIN_ARGS: str = "route, error"
ACCESS_WITHOUT_LOGIN_VALUES: list[ParameterSet] = [
    pytest.param(INVENTORY, get_error(INVENTORY), id="inventory_page"),
    # The error won't include the item id, so removing it
    pytest.param(
        INVENTORY_ITEM + PRODUCT_DETAIL_DATA[0][1],
        get_error(INVENTORY_ITEM.removesuffix("?id=")),
        id="inventory_item_page",
    ),
    pytest.param(CART, get_error(CART), id="cart_page"),
    pytest.param(
        CHECKOUT_STEP_1, get_error(CHECKOUT_STEP_1), id="checkout_step_1_page"
    ),
    pytest.param(
        CHECKOUT_STEP_2, get_error(CHECKOUT_STEP_2), id="checkout_step_2_page"
    ),
    pytest.param(
        CHECKOUT_COMPLETE, get_error(CHECKOUT_COMPLETE), id="checkout_complete_page"
    ),
]
