# fmt: off
import pytest
from playwright.sync_api import expect

from data.checkout_step_1_data import (
    ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR, CHECKOUT_ARGS,
    CHECKOUT_PARAMS, EMPTY_FIRST_NAME_ERROR, FIRST_NAME,
    FIRST_NAME_PLACEHOLDER, LAST_NAME, LAST_NAME_PLACEHOLDER, ZIP_CODE,
    ZIP_CODE_PLACEHOLDER)
from data.global_data import PLACEHOLDER
from data.routes import CART, CHECKOUT_STEP_1, CHECKOUT_STEP_2
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.login_page import LoginPage

from .form_validation_helpers import (assert_error_decorations,
                                      assert_no_error_decorations)

# fmt: on


def test_verify_first_name_textbox_placeholder(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    expect(checkout_step_1_page_with_item.first_name).to_have_attribute(
        name=PLACEHOLDER, value=FIRST_NAME_PLACEHOLDER
    )


def test_verify_last_name_textbox_placeholder(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    expect(checkout_step_1_page_with_item.last_name).to_have_attribute(
        name=PLACEHOLDER, value=LAST_NAME_PLACEHOLDER
    )


def test_verify_zip_code_textbox_placeholder(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    expect(checkout_step_1_page_with_item.zip_code).to_have_attribute(
        name=PLACEHOLDER, value=ZIP_CODE_PLACEHOLDER
    )


@pytest.mark.parametrize(CHECKOUT_ARGS, CHECKOUT_PARAMS)
def test_verify_checkout_error_with_empty_field(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
    first_name: str,
    last_name: str,
    zip_code: str,
    expected: str,
) -> None:
    assert_no_error_decorations(checkout_step_1_page_with_item)
    checkout_step_1_page_with_item.submit(first_name, last_name, zip_code)
    expect(checkout_step_1_page_with_item.form_validation.error_heading).to_have_text(
        expected
    )
    assert_error_decorations(checkout_step_1_page_with_item)


def test_verify_cancel_button_takes_user_back_to_cart_page(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_page_with_item.cancel()
    expect(cart_page.page).to_have_url(CART)


def test_verify_user_is_taken_to_checkout_step_2_after_successfully_filling_data_and_pressing_continue_button(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    checkout_step_1_page_with_item.submit(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    expect(checkout_step_1_page_with_item.page).to_have_url(CHECKOUT_STEP_2)


@pytest.mark.xfail(
    reason="Pressing Enter takes user back to cart_page, and not forward to checkout_step_two_page",
    raises=AssertionError,
    strict=True,
)
def test_verify_user_is_taken_to_checkout_step_2_after_successfully_filling_data_and_pressing_enter(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    checkout_step_1_page_with_item.submit_with_enter(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    expect(checkout_step_1_page_with_item.page).to_have_url(CHECKOUT_STEP_2)


def test_verify_error_dismissal_after_incomplete_fill_in(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> None:
    checkout_step_1_page_with_item.submit(first_name="", last_name="", zip_code="")
    expect(checkout_step_1_page_with_item.form_validation.error_heading).to_have_text(
        EMPTY_FIRST_NAME_ERROR
    )
    assert_error_decorations(checkout_step_1_page_with_item)
    checkout_step_1_page_with_item.form_validation.dismiss_error()
    assert_no_error_decorations(checkout_step_1_page_with_item)


@pytest.mark.anonymous
def test_verify_error_when_accessing_checkout_step_1_page_without_login(
    login_page: LoginPage,
) -> None:
    login_page.page.goto(CHECKOUT_STEP_1)
    expect(login_page.form_validation.error_heading).to_have_text(
        ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR
    )
