# fmt: off
import pytest
from playwright.sync_api import expect

from data.checkout_step_2_data import (PAYMENT_INFORMATION, PAYMENT_METHOD,
                                       PRICE_TOTAL_LABEL, SHIPPING_INFORMATION,
                                       SHIPPING_METHOD, SUBTOTAL_LABEL,
                                       TAX_LABEL, TOTAL_LABEL,
                                       calculate_subtotal, calculate_tax,
                                       calculate_total)
from data.routes import CHECKOUT_COMPLETE, INVENTORY
from po.pages.checkout_complete import CheckoutComplete
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from tests.shared_fixtures_names import (CHECKOUT_STEP_2_ORDER_ARGS,
                                         CHECKOUT_STEP_2_VALUES)

# fmt: on


def test_verify_payment_information(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    expect(checkout_step_2_page_with_item.payment_information).to_be_visible()
    expect(checkout_step_2_page_with_item.payment_information).to_have_text(
        PAYMENT_INFORMATION
    )

    expect(checkout_step_2_page_with_item.payment_method).to_be_visible()
    expect(checkout_step_2_page_with_item.payment_method).to_have_text(PAYMENT_METHOD)


def test_verify_shipping_information(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    expect(checkout_step_2_page_with_item.shipping_information).to_be_visible()
    expect(checkout_step_2_page_with_item.shipping_information).to_have_text(
        SHIPPING_INFORMATION
    )

    expect(checkout_step_2_page_with_item.shipping_method).to_be_visible()
    expect(checkout_step_2_page_with_item.shipping_method).to_have_text(SHIPPING_METHOD)


@pytest.mark.parametrize(CHECKOUT_STEP_2_ORDER_ARGS, CHECKOUT_STEP_2_VALUES)
def test_validate_order_pricing(
    request: pytest.FixtureRequest,
    page_fixture: str,
    items: dict[str, dict[str, str]],
) -> None:
    page: CheckoutStepTwoPage = request.getfixturevalue(page_fixture)

    expect.soft(page.price_total_label).to_be_visible()
    expect.soft(page.price_total_label).to_have_text(PRICE_TOTAL_LABEL)

    expected_subtotal: str = calculate_subtotal(items)
    expect.soft(page.subtotal).to_have_text(f"{SUBTOTAL_LABEL}{expected_subtotal}")

    expected_tax: str = calculate_tax(items)
    expect.soft(page.tax).to_have_text(f"{TAX_LABEL}{expected_tax}")

    expected_total: str = calculate_total(items)
    expect.soft(page.total).to_have_text(f"{TOTAL_LABEL}{expected_total}")


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
