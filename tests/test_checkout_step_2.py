# fmt: off
from data.cart_data import CART_ITEM_DATA
from data.checkout_step_2_data import calculate_subtotal, calculate_taxes
from data.inventory_data import INVENTORY_ITEMS_DATA
from po.pages.checkout_step_2_page import CheckoutStepTwoPage

# fmt: on


def test_validate_item_subtotal(
    checkout_step_2_with_item: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_item.get_subtotal() == calculate_subtotal(
        CART_ITEM_DATA
    )


def test_validate_all_items_total(
    checkout_step_2_with_all_items: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_all_items.get_subtotal() == calculate_subtotal(
        INVENTORY_ITEMS_DATA
    )


def test_verify_taxes_calculation_for_single_item(
    checkout_step_2_with_item: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_item.get_tax() == calculate_taxes(CART_ITEM_DATA)


def test_verify_taxes_calculation_for_all_items(
    checkout_step_2_with_all_items: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_all_items.get_tax() == calculate_taxes(
        INVENTORY_ITEMS_DATA
    )
