#fmt:off
from typing import Union

import pytest

from po.pages.base_page import INVENTORY_URL, LOGIN_URL
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

from .shared_fixtures_names import (EMPTY_FIXTURES, FIXTURES_WITH_ITEM,
                                    PAGE_FIXTURE)

#fmt:on


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_logout_from_all_menu_pages(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    login_page: LoginPage = page.menu.logout()
    assert login_page.get_url() == LOGIN_URL


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_all_items_from_all_menu_pages_with_empty_cart(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    inventory_page: InventoryPage = page.menu.all_items()
    assert inventory_page.get_url() == INVENTORY_URL
    assert inventory_page.cart.is_cart_empty()


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    FIXTURES_WITH_ITEM,
)
def test_all_items_from_all_menu_pages_with_item_in_cart(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    inventory_page: InventoryPage = page.menu.all_items()
    assert inventory_page.get_url() == INVENTORY_URL
    assert inventory_page.cart.get_cart_counter() == 1
