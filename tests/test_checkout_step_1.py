import pytest
from playwright.sync_api import expect

# fmt: off
from sauce_project.data.checkout_step_1_data import (
    ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR, EMPTY_FIRST_NAME_ERROR,
    EMPTY_LAST_NAME_ERROR, EMPTY_ZIP_CODE_ERROR, FIRST_NAME, LAST_NAME,
    ZIP_CODE)
# fmt: on
from sauce_project.po.pages.base_page import (
    CART_URL,
    CHECKOUT_STEP_1_URL,
    CHECKOUT_STEP_2_URL,
)
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.checkout_step_1_page import CheckoutStepOnePage
from sauce_project.tests.conftest import LoginPage


def test_01_verify_checkout_error_with_empty_first_name(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name="", last_name=LAST_NAME, zip_code=ZIP_CODE
        )
    assert EMPTY_FIRST_NAME_ERROR == str(exception.value)


def test_02_verify_checkout_error_with_empty_last_name(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name="", zip_code=ZIP_CODE
        )
    assert EMPTY_LAST_NAME_ERROR == str(exception.value)


def test_03_verify_checkout_error_with_empty_zip_code(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=""
        )
    assert EMPTY_ZIP_CODE_ERROR == str(exception.value)


def test_04_verify_cancel_button_takes_user_back_to_cart_page(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    cart_page: CartPage = checkout_step_1_with_item.get_cart_page()
    expect(cart_page._page).to_have_url(CART_URL)


def test_05_verify_user_is_taken_to_checkout_step_2_after_successfully_filling_data_and_pressing_continue_button(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    checkout_step_1_with_item.fill_in_checkout_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    expect(checkout_step_1_with_item._page).to_have_url(CHECKOUT_STEP_2_URL)


def test_06_verify_exception_when_accessing_checkout_step_1_page_error_without_login(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.attempt_access_unauthenticated(CHECKOUT_STEP_1_URL)
    assert ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR == str(exception.value)
