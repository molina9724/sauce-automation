from decimal import Decimal

from sauce_project.data.cart_data import FIRST_ITEM_KEY
from sauce_project.data.inventory_data import INVENTORY_ITEMS_DATA
from sauce_project.po.pages.checkout_step_2_page import CURRENCY

TOTAL_ITEM_VALUE: str = INVENTORY_ITEMS_DATA[FIRST_ITEM_KEY]["price"]


def add_all_prices(items: dict[str, dict[str, str]]) -> str:
    all_prices: list[str] = list()
    for internal_dict in items.values():
        all_prices.append(internal_dict["price"])

    all_prices_with_no_currency_sign: list[Decimal] = [
        Decimal(price[1:]) for price in all_prices
    ]
    total: Decimal = sum(all_prices_with_no_currency_sign, Decimal("0"))
    return f"{CURRENCY}{total:.2f}"
