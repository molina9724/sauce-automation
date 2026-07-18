import pytest
from playwright.sync_api import Locator, expect

# fmt: off
from sauce_project.data.checkout_step_1_data import (
    ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR, BACKGROUND, BORDER_BOTTOM,
    EMPTY_FIRST_NAME_ERROR, EMPTY_LAST_NAME_ERROR, EMPTY_ZIP_CODE_ERROR,
    FIRST_NAME, LAST_NAME, RED, ZIP_CODE)
from sauce_project.data.global_data import WHITE
from sauce_project.po.pages.base_page import (BACKGROUND_COLOR,
                                              BORDER_BOTTOM_COLOR, CART_URL,
                                              CHECKOUT_STEP_1_URL,
                                              CHECKOUT_STEP_2_URL, COLOR)
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.checkout_step_1_page import (ERROR_ICON,
                                                         CheckoutStepOnePage)
from sauce_project.po.pages.login_page import LoginPage

# fmt: on


def assert_error_decoration(page: CheckoutStepOnePage) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_visible()
        expect(container.locator(ERROR_ICON)).to_have_css(COLOR, RED)

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, BORDER_BOTTOM)

    expect(page.get_error_message_container()).to_have_css(BACKGROUND_COLOR, BACKGROUND)
    expect(page.get_error_heading()).to_have_css(COLOR, WHITE)


@pytest.mark.parametrize(
    "first, last, zip_code, expected",
    [
        ("", LAST_NAME, ZIP_CODE, EMPTY_FIRST_NAME_ERROR),
        (FIRST_NAME, "", ZIP_CODE, EMPTY_LAST_NAME_ERROR),
        (FIRST_NAME, LAST_NAME, "", EMPTY_ZIP_CODE_ERROR),
    ],
)
def test_checkout_error_with_empty_field(
    checkout_step_1_with_item, first, last, zip_code, expected
) -> None:
    with pytest.raises(RuntimeError) as exception:
        checkout_step_1_with_item.fill_in_checkout_information(first, last, zip_code)
    assert expected == str(exception.value)
    assert_error_decoration(checkout_step_1_with_item)


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
