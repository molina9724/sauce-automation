# fmt: off
from playwright.sync_api import expect

from data.cart_data import CART_ITEM_DATA
from po.components.cart_page_item import CartItem

# fmt: on


def verify_items_data(item: CartItem) -> bool:
    names: list[str] = list(CART_ITEM_DATA.keys())
    descriptions: list[str] = [key["description"] for key in CART_ITEM_DATA.values()]
    prices: list[str] = [key["price"] for key in CART_ITEM_DATA.values()]
    quantities = [details["quantity"] for details in CART_ITEM_DATA.values()]

    try:
        expect(item.name).to_have_text(names)
        expect(item.description).to_have_text(descriptions)
        expect(item.price).to_have_text(prices)
        expect(item.quantity).to_have_text(quantities)
        return True
    except AssertionError:
        return False
