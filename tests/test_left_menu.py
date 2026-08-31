#fmt:off
from typing import Union

import pytest
from playwright.sync_api import expect

from data.routes import INVENTORY, ROOT
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
    expect(login_page.page).to_have_url(ROOT)


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
    expect(inventory_page.page).to_have_url(INVENTORY)
    expect(inventory_page.cart.counter).to_be_hidden()


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
    expect(inventory_page.page).to_have_url(INVENTORY)
    expect(inventory_page.cart.counter).to_have_text("1")
