import pytest
from playwright.sync_api import Locator, Page, expect

from sauce_project.po.pages.base_page import BASE_URL
from sauce_project.po.pages.inventory_page import InventoryPage
# fmt: off
from sauce_project.po.pages.login_page import (EXPECTED_LOGIN_USERNAMES,
                                               PASSWORD, RANDOM_LOCKED_USER,
                                               RANDOM_UNBLOCKED_USER,
                                               SUCCESS_LOGIN_DATA,
                                               UNLOCKED_USERS, WRONG_PASSWORD,
                                               LoginPage)

# fmt: on


@pytest.fixture(scope="function", autouse=True)
def go_home(page: Page) -> Page:
    page.goto(BASE_URL)
    return page


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    return LoginPage(page)


@pytest.fixture
def inventory_page(page: Page) -> InventoryPage:
    return InventoryPage(page)


def test_01_document_title(login_page: LoginPage) -> None:
    assert login_page.get_document_title() == "Swag Labs"


def test_02_page_title(login_page: LoginPage) -> None:
    assert login_page.get_logo_text() == "Swag Labs"


def test_03_username_textbox_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_username_visible()


def test_04_password_textbox_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_password_visible()


def test_05_login_button_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_login_button_visible()


def test_06_usernames_heading_is_displayed(login_page: LoginPage) -> None:
    assert login_page.is_usernames_heading_visible()


def test_07_usernames(login_page: LoginPage) -> None:
    usernames: list[str] = login_page.get_credentials_usernames()
    assert usernames == EXPECTED_LOGIN_USERNAMES


def test_08_password_usernames_heading(login_page: LoginPage) -> None:
    heading: Locator = login_page._password_heading
    expect(heading).to_be_visible()
    expect(heading).to_have_text("Password for all users:")


def test_09_password(login_page: LoginPage) -> None:
    container: Locator = login_page._password_container
    text: str = container.inner_text()
    lines: list[str] = [line.strip() for line in text.splitlines() if line.strip()]

    if lines and lines[0].lower().startswith("password"):
        password = lines[1:]
    else:
        password: list[str] = lines

    assert password == ["secret_sauce"]


@pytest.mark.parametrize(
    "user, password, expected", argvalues=SUCCESS_LOGIN_DATA, ids=UNLOCKED_USERS
)
def test_10_successful_login_and_logout(
    login_page: LoginPage, inventory_page: InventoryPage, user, password, expected
):
    login_page.login(username=user, password=password)
    expect(login_page._page).to_have_url(expected)

    inventory_page._hamburger_button.click()
    inventory_page._logout_link.click()
    expect(login_page._page).to_have_url(BASE_URL)


def test_11_unsuccessful_login_empty_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    login_page.login(username="", password="")
    error: Locator = login_page._error_header
    expect(error).to_be_visible()
    expect(error).to_have_text("Epic sadface: Username is required")


def test_12_unsuccessful_login_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    login_page.login(username=RANDOM_UNBLOCKED_USER, password="")
    error: Locator = login_page._error_header
    expect(error).to_be_visible()
    expect(error).to_have_text("Epic sadface: Password is required")


def test_13_unsuccessful_login_empty_username_and_non_empty_password(
    login_page: LoginPage,
) -> None:
    login_page.login(username="", password=PASSWORD)
    error: Locator = login_page._error_header
    expect(error).to_be_visible()
    expect(error).to_have_text("Epic sadface: Username is required")


def test_14_unsuccessful_login_right_username_but_wrong_password(login_page: LoginPage):
    login_page.login(username=RANDOM_UNBLOCKED_USER, password=WRONG_PASSWORD)
    error: Locator = login_page._error_header
    expect(error).to_be_visible()
    expect(error).to_have_text(
        expected="Epic sadface: Username and password do not match any user in this service"
    )


def test_15_unsuccessful_login_with_locked_account(login_page: LoginPage) -> None:
    login_page.login(username=RANDOM_LOCKED_USER, password=PASSWORD)
    error: Locator = login_page._error_header
    expect(error).to_be_visible()
    expect(error).to_have_text(
        expected="Epic sadface: Sorry, this user has been locked out."
    )


def test_16_error_dismissal_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
):
    login_page.login(username="", password="")
    error: Locator = login_page._error_header
    expect(error).to_be_visible()

    close_error_button: Locator = login_page._close_error_button
    expect(close_error_button).to_be_visible()
    close_error_button.click()
    expect(close_error_button).to_be_hidden()


def test_17_error_clears_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    login_page.login(username="", password="")
    error: Locator = login_page._error_header
    expect(error).to_be_visible()

    close_error_button = login_page._close_error_button
    expect(close_error_button).to_be_visible()
    close_error_button.click()
    expect(close_error_button).to_be_hidden()


def test_18_password_field_masking(login_page: LoginPage) -> None:
    password_input: Locator = login_page._password
    expect(password_input).to_have_attribute(name="type", value="password")
    expect(password_input).to_have_attribute(name="type", value="password")
    expect(password_input).to_have_attribute(name="type", value="password")
