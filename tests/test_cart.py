from playwright.sync_api import expect

from sauce_project.po.pages.cart_page import CartPage

ITEM_INDEX: int = 0
ITEM_DATA: dict[str, dict[str, str]] = {
    "Sauce Labs Backpack": {
        "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        "price": "$29.99",
        "quantity": "1",
    }
}
ITEMS_AMOUNT = 6
ALL_ITEMS_INDEX: list[int] = [index for index in range(ITEMS_AMOUNT)]


def test_00_verify__cart_url(cart_page: CartPage) -> None:
    expect(cart_page._page).to_have_url("https://www.saucedemo.com/cart.html")


def test_01_cart_is_empty(empty_cart_page: CartPage) -> None:
    assert empty_cart_page.is_cart_empty()


def test_02_correct_item_in_cart(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_all_products_information() == ITEM_DATA


def test_03_item_is_removed(cart_page_with_item: CartPage) -> None:
    assert cart_page_with_item.get_amount_of_items_in_cart() == 1
    cart_page_with_item.remove_item(0)
    assert cart_page_with_item.is_cart_empty()
