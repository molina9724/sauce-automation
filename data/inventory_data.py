from typing import Callable, List

from data.item_data import INVENTORY_ITEMS_DATA

SortKey = Callable[[tuple[str, dict[str, str]]], str | float]

LEFT_MENU_ITEMS: List[str] = [
    "All Items",
    "Dynamic Catalog",
    "About",
    "Logout",
    "Reset App State",
]

# Filter options
A_TO_Z = "Name (A to Z)"
Z_TO_A = "Name (Z to A)"
LOW_TO_HIGH = "Price (low to high)"
HIGH_TO_LOW = "Price (high to low)"
FILTER_OPTIONS: List[str] = [
    A_TO_Z,
    Z_TO_A,
    LOW_TO_HIGH,
    HIGH_TO_LOW,
]
DEFAULT_FILTER_VALUE: str = FILTER_OPTIONS[0]

INDEX: str = "index"

PRODUCT_DETAIL_ARGS: str = "index, product_id"
PRODUCT_DETAIL_DATA: list[tuple[int, str]] = [
    (index, item["id"]) for index, item in enumerate(INVENTORY_ITEMS_DATA.values())
]
PRODUCT_DETAIL_IDS: list[str] = list(INVENTORY_ITEMS_DATA)

DOCUMENT_TITLE: str = "Swag Labs"
PRODUCTS_TITLE: str = "Products"
LOGO_TEXT: str = "Swag Labs"

ACCESS_INVENTORY_PAGE_ERROR_WITHOUT_LOGIN: str = (
    "Epic sadface: You can only access '/inventory.html' when you are logged in."
)


def get_price_value(item: tuple[str, dict[str, str]]) -> float:
    _, data = item
    price_text: str = data["price"]
    return float(price_text[1:])


def get_name_value(item: tuple[str, dict[str, str]]) -> str:
    name, _ = item
    return name


FILTER_ARGS: str = "filter_option, sort_key, reverse"
FILTER_VALUES: list[tuple[str, SortKey, bool]] = [
    (A_TO_Z, get_name_value, False),
    (Z_TO_A, get_name_value, True),
    (LOW_TO_HIGH, get_price_value, False),
    (HIGH_TO_LOW, get_price_value, True),
]

ZERO: int = 0


ITEMS_AMOUNT: int = len(INVENTORY_ITEMS_DATA)
ALL_ITEMS_INDEX: list[int] = list(range(ITEMS_AMOUNT))
