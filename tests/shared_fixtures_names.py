import pytest
from _pytest.mark.structures import ParameterSet

from data.cart_data import CART_ITEM_DATA, INVENTORY_ITEMS_DATA

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
ALL_FIXTURES: list[str] = FIXTURES_WITH_EMPTY_CART + FIXTURES_WITH_ITEM_IN_CART

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
CHECKOUT_STEP_2_FIXTURES: list[ParameterSet] = [
    pytest.param(
        "checkout_step_2_page_with_item",
        CART_ITEM_DATA,
        id="single_item",
    ),
    pytest.param(
        "checkout_step_2_page_with_all_items",
        INVENTORY_ITEMS_DATA,
        id="all_items",
    ),
]
