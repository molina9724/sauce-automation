from po.components.base_component import BaseComponent

BASE_URL: str = "https://www.saucedemo.com/"
LOGIN_URL: str = BASE_URL
INVENTORY_URL: str = BASE_URL + "inventory.html"
CART_URL: str = BASE_URL + "cart.html"
CHECKOUT_STEP_1_URL: str = BASE_URL + "checkout-step-one.html"
CHECKOUT_STEP_2_URL: str = BASE_URL + "checkout-step-two.html"


class BasePage(BaseComponent): ...
