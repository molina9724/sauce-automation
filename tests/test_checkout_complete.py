from playwright.sync_api import expect

from data.routes import CHECKOUT_COMPLETE
from po.pages.checkout_complete import CheckoutComplete


def test(checkout_complete_page_with_item: CheckoutComplete) -> None:
    expect(checkout_complete_page_with_item.page).to_have_url(CHECKOUT_COMPLETE)
