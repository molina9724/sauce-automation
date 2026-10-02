from data.item_data import INVENTORY_ITEMS_DATA

FIRST_ITEM_KEY: str = next(iter(INVENTORY_ITEMS_DATA))

# Cart shows everything inventory does, plus a quantity per item.
CART_ITEMS_DATA: dict[str, dict[str, str]] = {
    name: {**details, "quantity": "1"} for name, details in INVENTORY_ITEMS_DATA.items()
}
CART_ITEM_DATA: dict[str, dict[str, str]] = {
    FIRST_ITEM_KEY: CART_ITEMS_DATA[FIRST_ITEM_KEY]
}


YOUR_CART: str = "Your Cart"
QUANTITY: str = "QTY"
DESCRIPTION: str = "Description"
