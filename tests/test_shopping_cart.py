#fmt:off
import pytest

from sauce_project.tests.shared_fixtures_names import (EMPTY_FIXTURES,
                                                       FIXTURES_WITH_ITEM,
                                                       PAGE_FIXTURE)

from ..po.components.cart import Cart

#fmt:on


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    EMPTY_FIXTURES,
)
def test_shopping_cart_is_empty_from_all_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    cart: Cart = request.getfixturevalue(page_fixture)
    assert cart.is_cart_empty()


@pytest.mark.parametrize(
    PAGE_FIXTURE,
    FIXTURES_WITH_ITEM,
)
def test_shopping_cart_with_item_from_all_pages(
    page_fixture, request: pytest.FixtureRequest
) -> None:
    cart: Cart = request.getfixturevalue(page_fixture)
    assert cart.get_cart_counter() == 1
