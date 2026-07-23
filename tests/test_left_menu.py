import pytest

from sauce_project.po.components.left_menu import LeftMenu
from sauce_project.po.pages.base_page import LOGIN_URL
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage
from sauce_project.tests.left_menu_helpers import all_items, logout

PAGE_FIXTURE = "page_fixture"
EMPTY_FIXTURES: list[str] = [
    "empty_inventory_page",
    "empty_cart_page",
    "empty_checkout_step_1",
    "empty_checkout_step_2",
]

FIXTURES_WITH_ONE_ITEM: list[str] = [
    "inventory_page_with_item",
    "cart_page_with_item",
    "checkout_step_1_with_item",
    "checkout_step_2_with_item",
]


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_logout_from_all_menu_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: LeftMenu = request.getfixturevalue(page_fixture)
    login_page: LoginPage = logout(page)


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_all_items_from_all_menu_pages_with_empty_cart(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: LeftMenu = request.getfixturevalue(page_fixture)
    inventory_page: InventoryPage = all_items(page)
    assert inventory_page.is_cart_empty()


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    FIXTURES_WITH_ONE_ITEM,
)
def test_all_items_from_all_menu_pages_with_item_in_cart(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: LeftMenu = request.getfixturevalue(page_fixture)
    inventory_page: InventoryPage = all_items(page)
    assert inventory_page.get_cart_counter() == 1
