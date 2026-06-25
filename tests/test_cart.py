from playwright.sync_api import Locator, expect

from sauce_project.po.pages.cart_page import CartPage
from sauce_project.po.pages.inventory_page import InventoryPage

ITEM_INDEX: int = 0
ITEM_DATA: dict[str, str] = {
    "name": "Sauce Labs Backpack",
    "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
    "price": "$29.99",
}


def test_00_verify__cart_url(cart_page: CartPage) -> None:
    expect(cart_page._page).to_have_url("https://www.saucedemo.com/cart.html")


def test_01_item_is_added_to_cart(cart_page_with_item: CartPage) -> None:
    first_item: Locator = cart_page_with_item._page.locator(".cart_item")
    expect(first_item).to_have_count(1)

    amount: str = first_item.locator(".cart_quantity").inner_text().strip()
    assert amount == "1"
    name: str = first_item.locator(".inventory_item_name").inner_text().strip()
    assert name == ITEM_DATA["name"]
    description: str = first_item.locator(".inventory_item_desc").inner_text().strip()
    assert description == ITEM_DATA["description"]
    price: str = first_item.locator(".inventory_item_price").inner_text().strip()
    assert price == ITEM_DATA["price"]
