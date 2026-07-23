import pytest

from sauce_project.po.components.left_menu import LeftMenu
from sauce_project.tests.left_menu_helpers import logout

PAGE_FIXTURE = "page_fixture"
ALL_FIXTURES: list[str] = [
    "inventory_page",
    "empty_cart_page",
    "empty_checkout_step_1",
    "empty_checkout_step_2",
]


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    ALL_FIXTURES,
)
def test_logout_from_all_menu_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: LeftMenu = request.getfixturevalue(page_fixture)
    logout(page)
