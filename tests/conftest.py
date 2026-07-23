import pytest
from playwright.sync_api import Page

from sauce_project.data.cart_data import ALL_ITEMS_INDEX
# fmt: off
from sauce_project.data.checkout_step_1_data import (FIRST_NAME, LAST_NAME,
                                                     ZIP_CODE)
# fmt: on
from sauce_project.data.global_data import ITEM_INDEX
from sauce_project.data.login_data import DEFAULT_UNLOCKED_USER, PASSWORD
from sauce_project.po.pages.base_page import LOGIN_URL
from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.checkout_step_1_page import CheckoutStepOnePage
from sauce_project.po.pages.checkout_step_2_page import CheckoutStepTwoPage
from sauce_project.po.pages.inventory_page import InventoryPage
from sauce_project.po.pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.goto(LOGIN_URL)
    return login


@pytest.fixture
def empty_inventory_page(login_page: LoginPage) -> InventoryPage:
    return login_page.login(username=DEFAULT_UNLOCKED_USER, password=PASSWORD)


@pytest.fixture
def inventory_page_with_item(login_page: LoginPage) -> InventoryPage:
    inventory_page: InventoryPage = login_page.login(
        username=DEFAULT_UNLOCKED_USER, password=PASSWORD
    )
    inventory_page.add_item_to_cart(ITEM_INDEX)
    return inventory_page


@pytest.fixture
def inventory_page_with_all_items(login_page: LoginPage) -> InventoryPage:
    inventory_page: InventoryPage = login_page.login(
        username=DEFAULT_UNLOCKED_USER, password=PASSWORD
    )
    for index in ALL_ITEMS_INDEX:
        inventory_page.add_item_to_cart(index)
    return inventory_page


@pytest.fixture
def empty_cart_page(empty_inventory_page: InventoryPage) -> CartPage:
    cart_page: CartPage = empty_inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_item(empty_inventory_page: InventoryPage) -> CartPage:
    empty_inventory_page.add_item_to_cart(ITEM_INDEX)
    cart_page: CartPage = empty_inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_all_items(empty_inventory_page: InventoryPage) -> CartPage:
    for index in ALL_ITEMS_INDEX:
        empty_inventory_page.add_item_to_cart(index)
    cart_page: CartPage = empty_inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def empty_checkout_step_1(empty_cart_page: CartPage) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        empty_cart_page.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def checkout_step_1_with_item(cart_page_with_item: CartPage) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        cart_page_with_item.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def checkout_step_1_with_all_items(
    cart_page_with_all_items: CartPage,
) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        cart_page_with_all_items.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def empty_checkout_step_2(
    empty_checkout_step_1: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    checkout_step_2_with_item: CheckoutStepTwoPage = (
        empty_checkout_step_1.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
        )
    )
    return checkout_step_2_with_item


@pytest.fixture
def checkout_step_2_with_item(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    checkout_step_2_with_item: CheckoutStepTwoPage = (
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
        )
    )
    return checkout_step_2_with_item


@pytest.fixture
def checkout_step_2_with_all_items(
    checkout_step_1_with_all_items: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    checkout_step_2_with_item: CheckoutStepTwoPage = (
        checkout_step_1_with_all_items.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
        )
    )
    return checkout_step_2_with_item
