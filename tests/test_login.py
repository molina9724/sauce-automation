import random

import pytest
from playwright.sync_api import Locator, Page, expect

from sauce_project.po.pages.base_page import BASE_URL, INVENTORY_URL, LOGIN_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage

UNLOCKED_USERS = (
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
)
LOCKED_USERS = ("locked_out_user",)
ALL_USERS = (UNLOCKED_USERS[0],) + LOCKED_USERS + UNLOCKED_USERS[1:]
RANDOM_UNBLOCKED_USER = random.choice(UNLOCKED_USERS)
RANDOM_LOCKED_USER = random.choice(LOCKED_USERS)

PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong_password"

EXPECTED_LOGIN_USERNAMES = list(ALL_USERS)
SUCCESS_LOGIN_DATA = [(user, PASSWORD, INVENTORY_URL) for user in UNLOCKED_USERS]


@pytest.fixture(scope="function", autouse=True)
def go_home(page: Page) -> Page:
    page.goto(LOGIN_URL)
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
    usernames: list[str] = login_page.get_usernames()
    assert usernames == EXPECTED_LOGIN_USERNAMES


def test_08_password_usernames_heading(login_page: LoginPage) -> None:
    assert login_page.is_password_usernames_heading_displayed()


def test_09_password(login_page: LoginPage) -> None:
    assert login_page.get_password() == ["secret_sauce"]


@pytest.mark.parametrize(
    "user, password, expected", argvalues=SUCCESS_LOGIN_DATA, ids=UNLOCKED_USERS
)
def test_10_successful_login_and_logout(
    login_page: LoginPage, user, password, expected
):
    inventory_page: InventoryPage = login_page.login(username=user, password=password)
    expect(login_page._page).to_have_url(expected)
    inventory_page.logout()
    expect(login_page._page).to_have_url(BASE_URL)


def test_11_unsuccessful_login_empty_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username="", password="")
    assert "Epic sadface: Username is required" in str(exception_information.value)


def test_12_unsuccessful_login_username_and_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username=RANDOM_UNBLOCKED_USER, password="")
    assert "Epic sadface: Password is required" in str(exception_information.value)


def test_13_unsuccessful_login_empty_username_and_non_empty_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username="", password=PASSWORD)
    assert "Epic sadface: Username is required" in str(exception_information.value)


def test_14_unsuccessful_login_right_username_but_wrong_password(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username=RANDOM_UNBLOCKED_USER, password=WRONG_PASSWORD)
    assert (
        "Epic sadface: Username and password do not match any user in this service"
        in str(exception_information.value)
    )


def test_15_unsuccessful_login_with_locked_account(login_page: LoginPage) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username=RANDOM_LOCKED_USER, password=PASSWORD)
    assert "Epic sadface: Sorry, this user has been locked out" in str(
        exception_information.value
    )


def test_16_error_dismissal_after_unsuccessful_login_with_locked_account(
    login_page: LoginPage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        login_page.login(username="", password="")
    assert "Epic sadface: Username is required" in str(exception_information.value)
    assert login_page.is_error_displayed()
    login_page.dismiss_error()
    assert not login_page.is_error_displayed()


def test_18_password_field_masking(login_page: LoginPage) -> None:
    login_page.is_password_masked()
