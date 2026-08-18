# fmt: off
import pytest
from playwright.sync_api import expect

from data.login_data import (DOCUMENT_TITLE, EMPTY_USERNAME_ERROR,
                             EXPECTED_LOGIN_USERNAMES, LOGIN_ARGS,
                             LOGIN_ERROR_ARGS, LOGIN_ERROR_PARAMS, LOGO_TEXT,
                             PASSWORD, SUCCESS_LOGIN_DATA, UNLOCKED_USERS)
from po.pages.base_page import INVENTORY_URL
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

from .form_validation_helpers import (assert_error_decorations,
                                      assert_no_error_decorations)

# fmt: on

pytestmark: pytest.MarkDecorator = pytest.mark.anonymous


def test_verify_document_title(login_page: LoginPage) -> None:
    expect(login_page.page).to_have_title(DOCUMENT_TITLE)


def test_verify_page_title(login_page: LoginPage) -> None:
    expect(login_page.logo_heading).to_have_text(LOGO_TEXT)


def test_verify_username_textbox_is_displayed(login_page: LoginPage) -> None:
    expect(login_page.username).to_be_visible()


def test_verify_password_textbox_is_displayed(login_page: LoginPage) -> None:
    expect(login_page.password).to_be_visible()


def test_verify_login_button_is_displayed(login_page: LoginPage) -> None:
    expect(login_page.login_button).to_be_visible()


def test_verify_usernames_heading_is_displayed(login_page: LoginPage) -> None:
    expect(login_page.usernames_heading).to_be_visible()


def test_verify_usernames(login_page: LoginPage) -> None:
    usernames: list[str] = login_page.get_usernames()
    assert usernames == EXPECTED_LOGIN_USERNAMES


def test_verify_password_heading(login_page: LoginPage) -> None:
    expect(login_page.password_heading).to_be_visible()


def test_verify_password(login_page: LoginPage) -> None:
    assert login_page.get_password() == PASSWORD


@pytest.mark.parametrize(LOGIN_ARGS, argvalues=SUCCESS_LOGIN_DATA, ids=UNLOCKED_USERS)
def test_verify_successful_login(
    login_page: LoginPage, user: str, password: str
) -> None:
    inventory_page: InventoryPage = login_page.login(username=user, password=password)
    expect(inventory_page.page).to_have_url(INVENTORY_URL)


@pytest.mark.parametrize(LOGIN_ERROR_ARGS, LOGIN_ERROR_PARAMS)
def test_verify_unsuccessful_login(
    login_page: LoginPage, user: str, password: str, error: str
) -> None:
    login_page.submit_credentials(username=user, password=password)
    expect(login_page.form_validation.error_heading).to_have_text(error)
    assert_error_decorations(login_page)


def test_verify_error_dismissal_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    login_page.submit_credentials(username="", password="")
    expect(login_page.form_validation.error_heading).to_have_text(EMPTY_USERNAME_ERROR)
    assert_error_decorations(login_page)
    login_page.dismiss_error()
    assert_no_error_decorations(login_page)


def test_verify_password_field_masking(login_page: LoginPage) -> None:
    expect(login_page.password).to_have_attribute(name="type", value="password")
