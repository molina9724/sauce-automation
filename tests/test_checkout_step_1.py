from playwright.sync_api import expect

from sauce_project.po.pages.checkout_step_1 import CheckoutStepOnePage


def test_00(checkout_step_1_with_item: CheckoutStepOnePage) -> None:
    expect(checkout_step_1_with_item._page).to_have_url(
        "https://www.saucedemo.com/checkout-step-one.html"
    )
