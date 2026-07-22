# fmt: off
import pytest

from sauce_project.data.login_data import (DOCUMENT_TITLE,
                                           EMPTY_USERNAME_ERROR,
                                           EXPECTED_LOGIN_USERNAMES,
                                           LOGIN_ARGS, LOGIN_ERROR_ARGS,
                                           LOGIN_ERROR_PARAMS, LOGO_TEXT,
                                           PASSWORD, SUCCESS_LOGIN_DATA,
                                           UNLOCKED_USERS)
from sauce_project.po.pages.base_page import INVENTORY_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage
from sauce_project.tests.form_validation_mixin_helpers import (
    assert_error_decorations, assert_no_error_decorations)

# fmt: on


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
