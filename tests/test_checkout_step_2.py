# fmt: off
import pytest
from playwright.sync_api import expect

from data.checkout_step_2_data import (calculate_subtotal, calculate_taxes,
                                       calculate_total)
from data.routes import CHECKOUT_COMPLETE, INVENTORY
from po.pages.checkout_complete import CheckoutComplete
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from tests.shared_fixtures_names import (CHECKOUT_STEP_2_ORDER_ARGS,
                                         CHECKOUT_STEP_2_VALUES)

# fmt: on


@pytest.mark.parametrize(CHECKOUT_STEP_2_ORDER_ARGS, CHECKOUT_STEP_2_VALUES)
def test_validate_order_subtotal(
    request: pytest.FixtureRequest,
    page_fixture: str,
    items: dict[str, dict[str, str]],
) -> None:
    page: CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expected_subtotal: str = calculate_subtotal(items)
    expect(page.subtotal).to_contain_text(expected_subtotal)


@pytest.mark.parametrize(CHECKOUT_STEP_2_ORDER_ARGS, CHECKOUT_STEP_2_VALUES)
def test_validate_order_total(
    request: pytest.FixtureRequest,
    page_fixture: str,
    items: dict[str, dict[str, str]],
) -> None:
    page: CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expected_total: str = calculate_total(items)
    expect(page.total).to_contain_text(expected_total)


@pytest.mark.parametrize(CHECKOUT_STEP_2_ORDER_ARGS, CHECKOUT_STEP_2_VALUES)
def test_validate_order_taxes(
    request: pytest.FixtureRequest,
    page_fixture: str,
    items: dict[str, dict[str, str]],
) -> None:
    page: CheckoutStepTwoPage = request.getfixturevalue(page_fixture)
    expected_taxes: str = calculate_taxes(items)
    expect(page.tax).to_contain_text(expected_taxes)


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
