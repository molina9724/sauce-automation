# fmt: off
from playwright.sync_api import expect

from data.cart_data import CART_ITEM_DATA
from data.checkout_step_2_data import calculate_subtotal, calculate_taxes
from data.inventory_data import INVENTORY_ITEMS_DATA
from po.pages.checkout_step_2_page import CheckoutStepTwoPage

# fmt: on


def test_validate_item_subtotal(
    checkout_step_2_page_with_item: CheckoutStepTwoPage,
) -> None:
    expected_subtotal: str = calculate_subtotal(CART_ITEM_DATA)
    expect(checkout_step_2_page_with_item.subtotal).to_contain_text(expected_subtotal)


def test_validate_all_items_total(
    checkout_step_2_page_with_all_items: CheckoutStepTwoPage,
) -> None:
    expected_subtotal: str = calculate_subtotal(INVENTORY_ITEMS_DATA)
    expect(checkout_step_2_page_with_all_items.subtotal).to_contain_text(
        expected_subtotal
    )


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
