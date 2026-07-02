import pytest
from playwright.sync_api import Page

from sauce_project.data.cart_data import ALL_ITEMS_INDEX
from sauce_project.data.global_data import ITEM_INDEX
from sauce_project.data.login_data import DEFAULT_UNLOCKED_USER, PASSWORD

from ..po.pages.base_page import LOGIN_URL
from ..po.pages.cart_page import CartPage
from ..po.pages.checkout_step_1_page import CheckoutStepOnePage
from ..po.pages.inventory_page import InventoryPage
from ..po.pages.login_page import LoginPage


@pytest.fixture
def login_page(page: Page) -> LoginPage:
    page.goto(LOGIN_URL)
    return LoginPage(page)


@pytest.fixture
def inventory_page(login_page: LoginPage) -> InventoryPage:
    return login_page.login(username=DEFAULT_UNLOCKED_USER, password=PASSWORD)


@pytest.fixture
def empty_cart_page(inventory_page: InventoryPage) -> CartPage:
    cart_page: CartPage = inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_item(inventory_page: InventoryPage) -> CartPage:
    inventory_page.add_item_to_cart(ITEM_INDEX)
    cart_page: CartPage = inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def cart_page_with_all_items(inventory_page: InventoryPage) -> CartPage:
    for index in ALL_ITEMS_INDEX:
        inventory_page.add_item_to_cart(index)
    cart_page: CartPage = inventory_page.get_cart_page()
    return cart_page


@pytest.fixture
def checkout_step_1_with_item(cart_page_with_item: CartPage) -> CheckoutStepOnePage:
    checkout_step_1_page_with_item: CheckoutStepOnePage = (
        cart_page_with_item.get_checkout_step_1_page()
    )
    return checkout_step_1_page_with_item
