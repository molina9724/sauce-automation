from playwright.sync_api import expect

from data.item_data import ADD_TO_CART, INVENTORY_ITEMS_DATA, ITEM_INDEX, ONE, REMOVE
from po.pages.inventory_item_page import InventoryItemPage
from po.pages.inventory_page import InventoryPage
from tests.test_image import general_image_assert


def test_verify_right_item_is_displayed(empty_inventory_page: InventoryPage) -> None:
    name: str = list(INVENTORY_ITEMS_DATA.keys())[ITEM_INDEX]
    description: str = INVENTORY_ITEMS_DATA[name]["description"]
    price: str = INVENTORY_ITEMS_DATA[name]["price"]
    button: str = ADD_TO_CART
    item_image_alt: str = name

    inventory_item_page: InventoryItemPage = empty_inventory_page.open_item_by_name(
        ITEM_INDEX
    )

    expect(inventory_item_page.item.name).to_have_text(name)
    expect(inventory_item_page.item.description).to_have_text(description)
    expect(inventory_item_page.item.price).to_have_text(price)
    expect(inventory_item_page.item.button).to_have_text(button)
    expect(inventory_item_page.item.image).to_have_attribute(
        "alt", value=item_image_alt
    )
    general_image_assert(inventory_item_page, inventory_item_page.item.image)


def test_verify_item_can_be_added_to_cart(
    inventory_item_page: InventoryItemPage,
) -> None:
    expect(inventory_item_page.item.button).to_have_text(ADD_TO_CART)
    inventory_item_page.item.add()
    expect(inventory_item_page.cart.counter).to_have_text(str(ONE))
    expect(inventory_item_page.item.button).to_have_text(REMOVE)


def test_verify_item_can_be_removed_from_cart(
    inventory_item_page_with_item: InventoryItemPage,
) -> None:
    expect(inventory_item_page_with_item.item.button).to_have_text(REMOVE)
    inventory_item_page_with_item.item.remove()
    expect(inventory_item_page_with_item.cart.counter).to_be_hidden()
    expect(inventory_item_page_with_item.item.button).to_have_text(ADD_TO_CART)
