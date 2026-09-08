from playwright.sync_api import expect

from data.routes import INVENTORY
from po.pages.checkout_complete import CheckoutComplete
from po.pages.inventory_page import InventoryPage
from tests.test_image import general_image_assert


def test_verify_checkout_complete_message(
    checkout_complete_page_with_item: CheckoutComplete,
) -> None:
    expect(checkout_complete_page_with_item.title).to_be_visible()

    expect(checkout_complete_page_with_item.title).to_have_text("Checkout: Complete!")
    general_image_assert(
        checkout_complete_page_with_item,
        checkout_complete_page_with_item.heavy_check_mark,
    )
    expect(checkout_complete_page_with_item.header).to_have_text(
        "Thank you for your order!"
    )
    expect(checkout_complete_page_with_item.text).to_have_text(
        "Your order has been dispatched, and will arrive just as fast as the pony can get there!"
    )

    expect(checkout_complete_page_with_item.back_home_button).to_be_visible()


def test_verify_back_home_returns_to_empty_inventory_page(
    checkout_complete_page_with_item: CheckoutComplete,
) -> None:
    inventory_page: InventoryPage = (
        checkout_complete_page_with_item.get_inventory_page()
    )
    expect(inventory_page.page).to_have_url(INVENTORY)
    expect(inventory_page.cart.counter).to_be_hidden()
