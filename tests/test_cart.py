from playwright.sync_api import expect

from sauce_project.po.pages.cart_page import CartPage
from sauce_project.tests.test_inventory import INVENTORY_ITEMS_DATA

ITEM_INDEX: int = 0
ITEMS_AMOUNT: int = 6
ALL_ITEMS_INDEX: list[int] = [index for index in range(ITEMS_AMOUNT)]

FIRST_ITEM_KEY: str = next(iter(INVENTORY_ITEMS_DATA))
ITEM_DATA: dict[str, dict[str, str]] = {
    FIRST_ITEM_KEY: INVENTORY_ITEMS_DATA[FIRST_ITEM_KEY]
}
ITEMS_DATA: dict[str, dict[str, str]] = INVENTORY_ITEMS_DATA

KEY = "quantity"
VALUE = "1"
for key in ITEMS_DATA.keys():
    ITEMS_DATA[key][KEY] = VALUE


def test_00_verify__cart_url(empty_cart_page: CartPage) -> None:
    expect(empty_cart_page._page).to_have_url("https://www.saucedemo.com/cart.html")


def test_01_cart_is_empty(empty_cart_page: CartPage) -> None:
    assert empty_cart_page.is_cart_empty()


def test_02_correct_item_in_cart(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_all_products_information() == ITEM_DATA


def test_03_item_is_removed(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_amount_of_items_in_cart() == 1
    cart_page_with_item.remove_item(0)
    assert cart_page_with_item.is_cart_empty()


def test_04_several_items_in_cart(cart_page_with_all_items: CartPage) -> None:
    assert cart_page_with_all_items.get_amount_of_items_in_cart() == 6
