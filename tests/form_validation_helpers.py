#fmt:off
from typing import Union

from playwright.sync_api import expect

from data.form_validation_data import (BACKGROUND, BORDER_BOTTOM,
                                       DEFAULT_BORDER, RED)
from data.global_data import WHITE
from po.components.form_validation import (BACKGROUND_COLOR,
                                           BORDER_BOTTOM_COLOR, COLOR,
                                           ERROR_ICON)
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.login_page import LoginPage

#fmt:on


def assert_no_error_decorations(page: Union[LoginPage, CheckoutStepOnePage]) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_hidden()

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, DEFAULT_BORDER)

    expect(page.form_validation.error_message_container).not_to_be_visible()


def assert_error_decorations(page: Union[LoginPage, CheckoutStepOnePage]) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_visible()
        expect(container.locator(ERROR_ICON)).to_have_css(COLOR, RED)

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, BORDER_BOTTOM)

    expect(page.form_validation.error_message_container).to_have_css(
        BACKGROUND_COLOR, BACKGROUND
    )
    expect(page.form_validation.error_heading).to_have_css(COLOR, WHITE)
