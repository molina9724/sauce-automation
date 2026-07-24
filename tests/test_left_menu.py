#fmt:off
import pytest

from sauce_project.tests.shared_fixtures_names import (EMPTY_FIXTURES,
                                                       FIXTURES_WITH_ITEM,
                                                       PAGE_FIXTURE)

from ..po.components.left_menu import LeftMenu
from ..po.pages.inventory_page import InventoryPage
from ..po.pages.login_page import LoginPage
from ..tests.left_menu_helpers import all_items, logout

#fmt:on


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
    FIXTURES_WITH_ITEM,
)
def test_all_items_from_all_menu_pages_with_item_in_cart(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    page: LeftMenu = request.getfixturevalue(page_fixture)
    inventory_page: InventoryPage = all_items(page)
    assert inventory_page.get_cart_counter() == 1
