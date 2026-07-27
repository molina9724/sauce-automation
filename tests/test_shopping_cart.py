#fmt:off
from typing import Union

import pytest

from .shared_fixtures_names import (EMPTY_FIXTURES,
                                    FIXTURES_WITH_ITEM,
                                    PAGE_FIXTURE)

from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage

#fmt:on


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_shopping_cart_is_empty_from_all_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    assert page.cart.is_cart_empty()


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    FIXTURES_WITH_ITEM,
)
def test_shopping_cart_with_item_from_all_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: Union[InventoryPage, CartPage, CheckoutStepOnePage, CheckoutStepTwoPage] = (
        request.getfixturevalue(page_fixture)
    )
    assert page.cart.get_cart_counter() == 1
