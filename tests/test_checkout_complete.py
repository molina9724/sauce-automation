from playwright.sync_api import expect

from po.pages.checkout_complete import CheckoutComplete


def test_verify_checkout_complete_message(
    checkout_complete_page_with_item: CheckoutComplete,
) -> None:
    expect(checkout_complete_page_with_item.title).to_be_visible()
    expect(checkout_complete_page_with_item.title).to_have_text("Checkout: Complete!")
