# fmt: off
import pytest
from playwright.sync_api import expect

from data.checkout_step_1_data import (
    ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR, CHECKOUT_ARGS,
    CHECKOUT_IDS, CHECKOUT_PARAMS, FIRST_NAME, LAST_NAME, ZIP_CODE)
from po.pages.base_page import (CART_URL, CHECKOUT_STEP_1_URL,
                                CHECKOUT_STEP_2_URL)
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.login_page import LoginPage

from .form_validation_helpers import (assert_error_decorations,
                                      assert_no_error_decorations)

# fmt: on


@pytest.mark.parametrize(CHECKOUT_ARGS, CHECKOUT_PARAMS, ids=CHECKOUT_IDS)
def test_verify_checkout_error_with_empty_field(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
    first_name: str,
    last_name: str,
    zip_code: str,
    expected: str,
) -> None:
    assert_no_error_decorations(checkout_step_1_page_with_item)
    checkout_step_1_page_with_item.fill_in_checkout_information(
        first_name, last_name, zip_code
    )
    expect(checkout_step_1_page_with_item.form_validation.error_heading).to_have_text(
        expected
    )
    assert_error_decorations(checkout_step_1_page_with_item)


def test_verify_cancel_button_takes_user_back_to_cart_page(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_page_with_item.cart.get_cart_page()
    expect(cart_page.page).to_have_url(CART_URL)


def test_verify_user_is_taken_to_checkout_step_2_after_successfully_filling_data_and_pressing_continue_button(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    checkout_step_1_page_with_item.fill_in_checkout_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    expect(checkout_step_1_page_with_item.page).to_have_url(CHECKOUT_STEP_2_URL)


@pytest.mark.anonymous
def test_verify_error_when_accessing_checkout_step_1_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.goto(CHECKOUT_STEP_1_URL)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR
    )
