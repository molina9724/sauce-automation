from typing import List

LEFT_MENU_COMPONENTS: List[str] = ["All Items", "About", "Logout", "Reset App State"]

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

# Sorted by Name (A to Z) by default
INVENTORY_ITEMS_DATA: dict[str, dict[str, str]] = {
    "Sauce Labs Backpack": {
        "description": "carry.allTheThings() with the sleek, streamlined Sly Pack that melds uncompromising style with unequaled laptop and tablet protection.",
        "price": "$29.99",
    },
    "Sauce Labs Bike Light": {
        "description": "A red light isn't the desired state in testing but it sure helps when riding your bike at night. Water-resistant with 3 lighting modes, 1 AAA battery included.",
        "price": "$9.99",
    },
    "Sauce Labs Bolt T-Shirt": {
        "description": "Get your testing superhero on with the Sauce Labs bolt T-shirt. From American Apparel, 100% ringspun combed cotton, heather gray with red bolt.",
        "price": "$15.99",
    },
    "Sauce Labs Fleece Jacket": {
        "description": "It's not every day that you come across a midweight quarter-zip fleece jacket capable of handling everything from a relaxing day outdoors to a busy day at the office.",
        "price": "$49.99",
    },
    "Sauce Labs Onesie": {
        "description": "Rib snap infant onesie for the junior automation engineer in development. Reinforced 3-snap bottom closure, two-needle hemmed sleeved and bottom won't unravel.",
        "price": "$7.99",
    },
    "Test.allTheThings() T-Shirt (Red)": {
        "description": "This classic Sauce Labs t-shirt is perfect to wear when cozying up to your keyboard to automate a few tests. Super-soft and comfy ringspun combed cotton.",
        "price": "$15.99",
    },
}

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
