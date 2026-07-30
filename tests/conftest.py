import os

import pytest
from playwright.sync_api import Browser, BrowserContext, Page, expect

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

WORKER = os.environ.get("PYTEST_XDIST_WORKER", "master")
AUTH_FILE = f"./playwright/.auth/user_{WORKER}.json"


@pytest.fixture(scope="session", autouse=False)
def auto_login(browser: Browser):
    os.makedirs(os.path.dirname(AUTH_FILE), exist_ok=True)
    login_page: Page = browser.new_page()
    login_page.goto(LOGIN_URL)
    login_page.get_by_role("textbox", name="Username").fill(DEFAULT_UNLOCKED_USER)
    login_page.get_by_role("textbox", name="Password").fill(PASSWORD)
    login_page.get_by_role("button", name="Login").click()
    expect(login_page).to_have_url(INVENTORY_URL)
    login_page.context.storage_state(path=AUTH_FILE)
    login_page.close()

    yield
    os.remove(AUTH_FILE)


@pytest.fixture
def user_page(browser: Browser, auto_login):
    context: BrowserContext = browser.new_context(storage_state=AUTH_FILE)
    page: Page = context.new_page()
    yield page
    context.close()


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    login = LoginPage(page)
    login.goto(LOGIN_URL)
    return login


@pytest.fixture
def empty_inventory_page(user_page) -> InventoryPage:
    inventory_page = InventoryPage(user_page)
    inventory_page.goto(
        INVENTORY_URL,
    )
    return inventory_page


@pytest.fixture
def inventory_page_with_item(user_page) -> InventoryPage:
    inventory_page = InventoryPage(user_page)
    inventory_page.goto(INVENTORY_URL)
    inventory_page.add_item_to_cart(ITEM_INDEX)
    return inventory_page


@pytest.fixture
def inventory_page_with_all_items(user_page) -> InventoryPage:
    inventory_page = InventoryPage(user_page)
    inventory_page.goto(INVENTORY_URL)
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
