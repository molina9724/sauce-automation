from playwright.sync_api import expect

from sauce_project.po.pages.base_page import CHECKOUT_STEP_2_URL
from sauce_project.po.pages.checkout_step_2_page import CheckoutStepTwoPage


def test_00(checkout_step_2_with_item: CheckoutStepTwoPage) -> None:
    expect(checkout_step_2_with_item._page).to_have_url(CHECKOUT_STEP_2_URL)
