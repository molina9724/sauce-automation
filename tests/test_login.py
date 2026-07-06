import pytest
from playwright.sync_api import expect

# fmt: off
from sauce_project.data.login_data import (DEFAULT_BLOCKED_USER,
                                           DEFAULT_UNLOCKED_USER,
                                           DOCUMENT_TITLE,
                                           EMPTY_PASSWORD_ERROR,
                                           EMPTY_USERNAME_ERROR,
                                           EXPECTED_LOGIN_USERNAMES,
                                           LOCKED_ACCOUNT_ERROR, LOGO_TEXT,
                                           PASSWORD, SUCCESS_LOGIN_DATA,
                                           UNLOCKED_USERS,
                                           WRONG_CREDENTIALS_ERROR,
                                           WRONG_PASSWORD)
# fmt: on
from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


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


@pytest.mark.parametrize(
    "user, password, expected", argvalues=SUCCESS_LOGIN_DATA, ids=UNLOCKED_USERS
)
def test_10_verify_successful_login_and_logout(
    login_page: LoginPage, user, password, expected
) -> None:
    inventory_page: InventoryPage = login_page.login(username=user, password=password)
    expect(login_page._page).to_have_url(expected)
    inventory_page.logout()
    expect(login_page._page).to_have_url(BASE_URL)


def test_11_verify_unsuccessful_login_empty_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username="", password="")
    assert EMPTY_USERNAME_ERROR == str(exception.value)


def test_12_verify_unsuccessful_login_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username=DEFAULT_UNLOCKED_USER, password="")
    assert EMPTY_PASSWORD_ERROR == str(exception.value)


def test_13_verify_unsuccessful_login_empty_username_and_non_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username="", password=PASSWORD)
    assert EMPTY_USERNAME_ERROR == str(exception.value)


def test_14_verify_unsuccessful_login_right_username_but_wrong_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username=DEFAULT_UNLOCKED_USER, password=WRONG_PASSWORD)
    assert WRONG_CREDENTIALS_ERROR == str(exception.value)


def test_15_verify_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username=DEFAULT_BLOCKED_USER, password=PASSWORD)
    assert LOCKED_ACCOUNT_ERROR == str(exception.value)


def test_16_verify_error_dismissal_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception:
        login_page.login(username="", password="")
    assert EMPTY_USERNAME_ERROR == str(exception.value)
    assert login_page.is_error_displayed()
    login_page.dismiss_error()
    assert not login_page.is_error_displayed()


def test_17_verify_password_field_masking(login_page: LoginPage) -> None:
    assert login_page.is_password_masked()
