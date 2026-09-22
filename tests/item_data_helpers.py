from playwright.sync_api import expect

from po.components.cart_item import CartItem


def verify_items_data(item: CartItem, data: dict[str, dict[str, str]]) -> None:
    names: list[str] = list(data.keys())
    descriptions: list[str] = [key["description"] for key in data.values()]
    prices: list[str] = [key["price"] for key in data.values()]
    quantities: list[str] = [details["quantity"] for details in data.values()]

    expect(item.name).to_have_text(names)
    expect(item.description).to_have_text(descriptions)
    expect(item.price).to_have_text(prices)
    expect(item.quantity).to_have_text(quantities)
