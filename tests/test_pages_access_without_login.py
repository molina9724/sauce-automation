import pytest
from playwright.sync_api import expect

from data.routes import ROOT
from po.pages.login_page import LoginPage
from tests.shared_fixtures_names import (
    ACCESS_WITHOUT_LOGIN_ARGS,
    ACCESS_WITHOUT_LOGIN_VALUES,
)


@pytest.mark.anonymous
@pytest.mark.parametrize(ACCESS_WITHOUT_LOGIN_ARGS, ACCESS_WITHOUT_LOGIN_VALUES)
def test_verify_error_when_trying_to_access_pages_without_login(
    login_page: LoginPage, route: str, error: str
) -> None:
    login_page.page.goto(route)
    expect(login_page.form_validation.error_heading).to_have_text(error)
    expect(login_page.page).to_have_url(ROOT)
