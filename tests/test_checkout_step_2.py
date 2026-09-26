# fmt: off
import pytest
from playwright.sync_api import expect

from data.cart_data import CART_ITEM_DATA
from data.checkout_step_2_data import (calculate_subtotal, calculate_taxes,
                                       calculate_total)
from data.item_data import INVENTORY_ITEMS_DATA
from data.routes import CHECKOUT_COMPLETE, INVENTORY
from po.pages.checkout_complete import CheckoutComplete
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from tests.shared_fixtures_names import (CHECKOUT_STEP_2_FIXTURES,
                                         CHECKOUT_STEP_2_ORDER_ARGS)

# fmt: on


@pytest.mark.parametrize(CHECKOUT_STEP_2_ORDER_ARGS, CHECKOUT_STEP_2_FIXTURES)
def test_validate_order_subtotal(
    request: pytest.FixtureRequest,
    page_fixture: str,
    items: dict[str, dict[str, str]],
) -> None:
    page: CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expected_subtotal: str = calculate_subtotal(items)
    expect(page.subtotal).to_contain_text(expected_subtotal)


def test_validate_item_total(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    expected_total: str = calculate_total(CART_ITEM_DATA)
    expect(checkout_step_2_page_with_item.total).to_contain_text(expected_total)


def test_validate_all_items_total(
    checkout_step_2_page_with_all_items: CheckoutStepTwoPage,
) -> None:
    expected_total: str = calculate_total(INVENTORY_ITEMS_DATA)
    expect(checkout_step_2_page_with_all_items.total).to_contain_text(expected_total)


def test_verify_taxes_calculation_for_single_item(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    expected_taxes: str = calculate_taxes(CART_ITEM_DATA)
    expect(checkout_step_2_page_with_item.tax).to_contain_text(expected_taxes)


def test_verify_taxes_calculation_for_all_items(
    checkout_step_2_page_with_all_items: CheckoutStepTwoPage,
) -> None:
    expected_taxes: str = calculate_taxes(INVENTORY_ITEMS_DATA)
    expect(checkout_step_2_page_with_all_items.tax).to_contain_text(expected_taxes)


def test_verify_cancel_button_takes_user_to_inventory_page(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    inventory_page: InventoryPage = checkout_step_2_page_with_item.cancel()
    expect(inventory_page.page).to_have_url(INVENTORY)


def test_verify_finish_button_takes_user_to_checkout_complete_page(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    checkout_complete: CheckoutComplete = checkout_step_2_page_with_item.finish()
    expect(checkout_complete.page).to_have_url(CHECKOUT_COMPLETE)
