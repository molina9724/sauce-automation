from sauce_project.data.cart_data import CART_ITEM_DATA
# fmt: off
from sauce_project.data.checkout_step_2_data import (add_all_prices,
                                                     calculate_taxes)
# fmt: on
from sauce_project.data.inventory_data import INVENTORY_ITEMS_DATA
from sauce_project.po.pages.checkout_step_2_page import CheckoutStepTwoPage


def test_01_validate_item_total(checkout_step_2_with_item: CheckoutStepTwoPage) -> None:
    assert checkout_step_2_with_item.calculate_item_total() == add_all_prices(
        CART_ITEM_DATA
    )


def test_02_validate_all_items_total(
    checkout_step_2_with_all_items: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_all_items.calculate_item_total() == add_all_prices(
        INVENTORY_ITEMS_DATA
    )


def test_03_verify_taxes_calculation_for_single_item(
    checkout_step_2_with_item: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_item.calculate_taxes() == calculate_taxes(
        CART_ITEM_DATA
    )


def test_04_verify_taxes_calculation_for_all_items(
    checkout_step_2_with_all_items: CheckoutStepTwoPage,
) -> None:
    assert checkout_step_2_with_all_items.calculate_taxes() == calculate_taxes(
        INVENTORY_ITEMS_DATA
    )
