#fmt:off
from typing import Union

import pytest
from playwright.sync_api import expect

from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage

from .shared_fixtures_names import (EMPTY_FIXTURES, FIXTURES_WITH_ITEM,
                                    PAGE_FIXTURE)

#fmt:on


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
    ids=EMPTY_FIXTURES,
)
def test_shopping_cart_is_empty_from_all_pages(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    expect(page.cart.counter).to_be_hidden()


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    FIXTURES_WITH_ITEM,
    ids=FIXTURES_WITH_ITEM,
)
def test_shopping_cart_with_item_from_all_pages(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    expect(page.cart.counter).to_have_text("1")
