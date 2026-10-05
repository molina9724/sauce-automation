# fmt: off
from typing import Union

import pytest
from playwright.sync_api import expect

from data.global_data import DOCUMENT_TITLE, LOGO_TEXT
from po.pages.cart_page import CartPage
from po.pages.checkout_complete import CheckoutComplete
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_item_page import InventoryItemPage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage
from tests.shared_fixtures_names import (GLOBAL_PAGE_FIXTURES,
                                         GLOBAL_SUBTITLE_ARGS,
                                         GLOBAL_SUBTITLE_VALUES, PAGE_FIXTURE)

# fmt: on


@pytest.mark.parametrize(PAGE_FIXTURE, GLOBAL_PAGE_FIXTURES)
def test_verify_document_title(
    page_fixture: str, request: pytest.FixtureRequest
) -> None:
    page: Union[
        LoginPage,
        InventoryPage,
        InventoryItemPage,
        CartPage,
        CheckoutStepOnePage,
        CheckoutStepTwoPage,
        CheckoutComplete,
    ] = request.getfixturevalue(page_fixture)
    expect(page.page).to_have_title(DOCUMENT_TITLE)


@pytest.mark.parametrize(PAGE_FIXTURE, GLOBAL_PAGE_FIXTURES)
def test_verify_page_logo(page_fixture: str, request: pytest.FixtureRequest) -> None:
    page: Union[
        LoginPage,
        InventoryPage,
        InventoryItemPage,
        CartPage,
        CheckoutStepOnePage,
        CheckoutStepTwoPage,
        CheckoutComplete,
    ] = request.getfixturevalue(page_fixture)
    expect(page.logo).to_have_text(LOGO_TEXT)


@pytest.mark.parametrize(GLOBAL_SUBTITLE_ARGS, GLOBAL_SUBTITLE_VALUES)
def test_verify_page_title(
    page_fixture: str, request: pytest.FixtureRequest, has_subtitle: bool, subtitle: str
) -> None:
    page: Union[
        LoginPage,
        InventoryPage,
        InventoryItemPage,
        CartPage,
        CheckoutStepOnePage,
        CheckoutStepTwoPage,
        CheckoutComplete,
    ] = request.getfixturevalue(page_fixture)
    if has_subtitle:
        expect(page.locator(".title")).to_have_text(subtitle)
    else:
        expect(page.locator(".title")).to_be_hidden()
