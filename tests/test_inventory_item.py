from playwright.sync_api import expect

from data.inventory_data import ADD_TO_CART, INVENTORY_ITEMS_DATA, ITEM_INDEX
from po.pages.inventory_item_page import InventoryItemPage
from po.pages.inventory_page import InventoryPage


def test_verify_right_item_is_displayed(empty_inventory_page: InventoryPage) -> None:
    name: str = list(INVENTORY_ITEMS_DATA.keys())[ITEM_INDEX]
    description: str = INVENTORY_ITEMS_DATA[name]["description"]
    price: str = INVENTORY_ITEMS_DATA[name]["price"]
    button: str = ADD_TO_CART

    # TODO: Compare images

    inventory_item_page: InventoryItemPage = empty_inventory_page.open_item_by_name(
        ITEM_INDEX
    )

    expect(inventory_item_page.item.name).to_have_text(name)
    expect(inventory_item_page.item.description).to_have_text(description)
    expect(inventory_item_page.item.price).to_have_text(price)
    expect(inventory_item_page.item.button).to_have_text(button)
