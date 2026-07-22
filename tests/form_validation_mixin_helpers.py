from playwright.sync_api import expect

from sauce_project.data.form_validation_mixin_data import (
    BACKGROUND,
    BORDER_BOTTOM,
    DEFAULT_BORDER,
    RED,
)
from sauce_project.data.global_data import WHITE
from sauce_project.po.components.form_validation_mixin import (
    ERROR_ICON,
    FormValidationMixIn,
)
from sauce_project.po.pages.base_page import (
    BACKGROUND_COLOR,
    BORDER_BOTTOM_COLOR,
    COLOR,
    SHORT_TIMEOUT,
)


# Helpers
def assert_no_error_decorations(page: FormValidationMixIn) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_hidden()

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, DEFAULT_BORDER)

    assert not page.is_error_container_displayed(SHORT_TIMEOUT)


def assert_error_decorations(page: FormValidationMixIn) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_visible()
        expect(container.locator(ERROR_ICON)).to_have_css(COLOR, RED)

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, BORDER_BOTTOM)

    expect(page.get_error_message_container()).to_have_css(BACKGROUND_COLOR, BACKGROUND)
    expect(page.get_error_heading()).to_have_css(COLOR, WHITE)
