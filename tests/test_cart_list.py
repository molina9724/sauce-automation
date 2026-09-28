import pytest
from playwright.sync_api import expect

from data.cart_data import CART_ITEMS_DATA, DESCRIPTION, QUANTITY
from data.inventory_data import ALL_ITEMS_INDEX
from po.pages.cart_page import CartPage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from tests.item_data_helpers import verify_items_data
from tests.shared_fixtures_names import CART_LIST_FIXTURES, PAGE_FIXTURE


@pytest.mark.parametrize(PAGE_FIXTURE, CART_LIST_FIXTURES)
def test_verify_correct_items_in_page(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: CartPage | CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    verify_items_data(page.cart_list.item, CART_ITEMS_DATA)


@pytest.mark.parametrize(PAGE_FIXTURE, CART_LIST_FIXTURES)
def test_verify_cart_list_headers(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: CartPage | CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expect(page.cart_list.quantity).to_have_text(QUANTITY)
    expect(page.cart_list.description).to_have_text(DESCRIPTION)


@pytest.mark.parametrize(PAGE_FIXTURE, CART_LIST_FIXTURES)
def test_verify_several_items_can_be_added(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: CartPage | CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expect(page.cart_list.item.root).to_have_count(len(ALL_ITEMS_INDEX))
