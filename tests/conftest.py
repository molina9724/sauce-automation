import os
from pathlib import Path

import pytest
from playwright.sync_api import Browser, BrowserContext, Page

from data.cart_data import ALL_ITEMS_INDEX
from data.checkout_step_1_data import FIRST_NAME, LAST_NAME, ZIP_CODE
from data.global_data import ITEM_INDEX
from data.login_data import DEFAULT_UNLOCKED_USER, PASSWORD
from po.pages.base_page import INVENTORY_URL, LOGIN_URL
from po.pages.cart_page import CartPage
from po.pages.checkout_step_1_page import CheckoutStepOnePage
from po.pages.checkout_step_2_page import CheckoutStepTwoPage
from po.pages.inventory_page import InventoryPage
from po.pages.login_page import LoginPage

WORKER: str = os.environ.get("PYTEST_XDIST_WORKER", "master")


@pytest.fixture(scope="session")
def auth_state_path(browser: Browser):
    path = Path(f"./playwright/.auth/user_{WORKER}_{browser.browser_type.name}.json")
    path.parent.mkdir(parents=True, exist_ok=True)

    context: BrowserContext = browser.new_context()
    login_page: LoginPage = LoginPage(context.new_page())
    login_page.page.goto(LOGIN_URL)
    login_page.login(DEFAULT_UNLOCKED_USER, PASSWORD)
    context.storage_state(path=path)
    context.close()

    yield path
    path.unlink(missing_ok=True)


@pytest.fixture
def browser_context_args(browser_context_args, request):
    if request.node.get_closest_marker("anonymous"):
        return browser_context_args
    auth = request.getfixturevalue("auth_state_path")
    return {**browser_context_args, "storage_state": str(auth)}


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.page.goto(LOGIN_URL)
    return login


@pytest.fixture
def empty_inventory_page(page: Page) -> InventoryPage:
    inventory_page = InventoryPage(page)
    inventory_page.page.goto(
        INVENTORY_URL,
    )
    return inventory_page


@pytest.fixture
def inventory_page_with_item(page: Page) -> InventoryPage:
    inventory_page = InventoryPage(page)
    inventory_page.page.goto(INVENTORY_URL)
    inventory_page.add_item_to_cart(ITEM_INDEX)
    return inventory_page


@pytest.fixture
def inventory_page_with_all_items(page: Page) -> InventoryPage:
    inventory_page = InventoryPage(page)
    inventory_page.page.goto(INVENTORY_URL)
    for index in ALL_ITEMS_INDEX:
        inventory_page.add_item_to_cart(index)
    return inventory_page


@pytest.fixture
def empty_cart_page(empty_inventory_page: InventoryPage) -> CartPage:
    cart_page: CartPage = empty_inventory_page.cart.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_item(empty_inventory_page: InventoryPage) -> CartPage:
    empty_inventory_page.add_item_to_cart(ITEM_INDEX)
    cart_page: CartPage = empty_inventory_page.cart.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_all_items(empty_inventory_page: InventoryPage) -> CartPage:
    for index in ALL_ITEMS_INDEX:
        empty_inventory_page.add_item_to_cart(index)
    cart_page: CartPage = empty_inventory_page.cart.get_cart_page()
    return cart_page


@pytest.fixture
def empty_checkout_step_1_page(empty_cart_page: CartPage) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        empty_cart_page.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def checkout_step_1_page_with_item(
    cart_page_with_item: CartPage,
) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        cart_page_with_item.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def checkout_step_1_page_with_all_items(
    cart_page_with_all_items: CartPage,
) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        cart_page_with_all_items.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item


@pytest.fixture
def empty_checkout_step_2_page(
    empty_checkout_step_1_page: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    empty_checkout_step_1_page.fill_in_checkout_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    empty_checkout_step_2_page: CheckoutStepTwoPage = (
        empty_checkout_step_1_page.get_checkout_step_two_page()
    )
    return empty_checkout_step_2_page


@pytest.fixture
def checkout_step_2_page_with_item(
    checkout_step_1_page_with_item: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    checkout_step_1_page_with_item.fill_in_checkout_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    checkout_step_2_page_with_item: CheckoutStepTwoPage = (
        checkout_step_1_page_with_item.get_checkout_step_two_page()
    )
    return checkout_step_2_page_with_item


@pytest.fixture
def checkout_step_2_page_with_all_items(
    checkout_step_1_page_with_all_items: CheckoutStepOnePage,
) -> CheckoutStepTwoPage:
    checkout_step_1_page_with_all_items.fill_in_checkout_information(
        first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=ZIP_CODE
    )
    checkout_step_2_all_items: CheckoutStepTwoPage = (
        checkout_step_1_page_with_all_items.get_checkout_step_two_page()
    )
    return checkout_step_2_all_items
