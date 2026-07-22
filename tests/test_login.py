# fmt: off
import pytest
from playwright.sync_api import expect

from sauce_project.data.global_data import (BACKGROUND, BORDER_BOTTOM,
                                            DEFAULT_BORDER, RED, WHITE)
from sauce_project.data.login_data import (DOCUMENT_TITLE,
                                           EMPTY_USERNAME_ERROR,
                                           EXPECTED_LOGIN_USERNAMES,
                                           LOGIN_ARGS, LOGIN_ERROR_ARGS,
                                           LOGIN_ERROR_PARAMS, LOGO_TEXT,
                                           PASSWORD, SUCCESS_LOGIN_DATA,
                                           UNLOCKED_USERS)
from sauce_project.po.components.form_validation_mixin import ERROR_ICON
from sauce_project.po.pages.base_page import (BACKGROUND_COLOR,
                                              BORDER_BOTTOM_COLOR, COLOR,
                                              INVENTORY_URL)
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import SHORT_TIMEOUT, LoginPage

# fmt: on


def assert_no_error_decorations(page: LoginPage) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_hidden()

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, DEFAULT_BORDER)

    assert not page.is_error_container_displayed(SHORT_TIMEOUT)


def assert_error_decorations(page: LoginPage) -> None:
    for container in page.get_fields_containers():
        expect(container.locator(ERROR_ICON)).to_be_visible()
        expect(container.locator(ERROR_ICON)).to_have_css(COLOR, RED)

    for field in page.get_fields():
        expect(field).to_have_css(BORDER_BOTTOM_COLOR, BORDER_BOTTOM)

    expect(page.get_error_message_container()).to_have_css(BACKGROUND_COLOR, BACKGROUND)
    expect(page.get_error_heading()).to_have_css(COLOR, WHITE)


def test_01_verify_document_title(login_page: LoginPage) -> None:
    assert login_page.get_document_title() == DOCUMENT_TITLE


def test_02_verify_page_title(login_page: LoginPage) -> None:
    assert login_page.get_logo_text() == LOGO_TEXT


def test_03_verify_username_textbox_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_username_displayed()


def test_04_verify_password_textbox_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_password_displayed()


def test_05_verify_login_button_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_login_button_displayed()


def test_06_verify_usernames_heading_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_usernames_heading_displayed()


def test_07_verify_usernames(login_page: LoginPage) -> None:
    usernames: list[str] = login_page.get_usernames()
    assert usernames == EXPECTED_LOGIN_USERNAMES


def test_08_verify_password_heading(login_page: LoginPage) -> None:
    assert login_page.is_password_heading_displayed()


def test_09_verify_password(login_page: LoginPage) -> None:
    assert login_page.get_password() == PASSWORD


@pytest.mark.parametrize(LOGIN_ARGS, argvalues=SUCCESS_LOGIN_DATA, ids=UNLOCKED_USERS)
def test_10_verify_successful_login(login_page: LoginPage, user, password) -> None:
    assert_no_error_decorations(login_page)
    inventory_page: InventoryPage = login_page.login(username=user, password=password)
    assert inventory_page.get_url() == INVENTORY_URL


@pytest.mark.parametrize(LOGIN_ERROR_ARGS, LOGIN_ERROR_PARAMS)
def test_11_verify_unsuccessful_login(
    login_page: LoginPage, user, password, error
) -> None:
    assert_no_error_decorations(login_page)
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username=user, password=password)
    assert_error_decorations(login_page)
    assert error == str(exception.value)


def test_16_verify_error_dismissal_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username="", password="")
    assert EMPTY_USERNAME_ERROR == str(exception.value)
    assert login_page.is_error_displayed()
    login_page.dismiss_error()
    assert_no_error_decorations(login_page)
    assert not login_page.is_error_displayed()


def test_17_verify_password_field_masking(login_page: LoginPage) -> None:
    assert login_page.is_password_masked()
