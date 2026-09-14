#fmt:off
from typing import Union

import pytest
from playwright.sync_api import expect

from data.routes import INVENTORY, ROOT
from po.pages.cart_page import CartPage
from po.pages.checkout_complete import CheckoutComplete
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

from .shared_fixtures_names import (ALL_FIXTURES, MENU_PAGE_FIXTURES,
                                    PAGE_FIXTURE)

#fmt:on


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    ALL_FIXTURES,
)
def test_logout_from_all_menu_pages(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[
        InventoryPage,
        CartPage,
        CheckoutStepOnePage,
        CheckoutStepTwoPage,
        CheckoutComplete,
    ] = request.getfixturevalue(page_fixture)
    login_page: LoginPage = page.menu.logout()
    expect(login_page.page).to_have_url(ROOT)


@pytest.mark.parametrize("page_fixture, cart_has_item", MENU_PAGE_FIXTURES)
def test_all_items_from_all_menu_pages(
    page_fixture: str,
    cart_has_item: bool,
    request: pytest.FixtureRequest,
) -> None:
    page: Union[
        InventoryPage,
        CartPage,
        CheckoutStepOnePage,
        CheckoutStepTwoPage,
        CheckoutComplete,
    ] = request.getfixturevalue(page_fixture)
    inventory_page: InventoryPage = page.menu.all_items()

    expect(inventory_page.page).to_have_url(INVENTORY)

    if cart_has_item:
        expect(inventory_page.cart.counter).to_have_text("1")
    else:
        expect(inventory_page.cart.counter).to_be_hidden()
