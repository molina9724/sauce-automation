from typing import List

from sauce_project.po.pages.base_page import INVENTORY_URL

# Global data
# --------------------------------------------------------------------------------------------------------------

ITEM_INDEX: int = 0
ITEMS_AMOUNT: int = 6

# --------------------------------------------------------------------------------------------------------------

# Data for test_login
# --------------------------------------------------------------------------------------------------------------

PERFORMANCE_GLITCHED_USER = "performance_glitch_user"

UNLOCKED_USERS = (
    "standard_user",
    "problem_user",
    "performance_glitch_user",
    "error_user",
    "visual_user",
)
LOCKED_USERS = ("locked_out_user",)

DEFAULT_UNLOCKED_USER = "standard_user"
DEFAULT_BLOCKED_USER = "locked_out_user"
ALL_USERS = (UNLOCKED_USERS[0],) + LOCKED_USERS + UNLOCKED_USERS[1:]

PASSWORD = "secret_sauce"
WRONG_PASSWORD = "wrong_password"

EXPECTED_LOGIN_USERNAMES = list(ALL_USERS)
SUCCESS_LOGIN_DATA = [(user, PASSWORD, INVENTORY_URL) for user in UNLOCKED_USERS]

# --------------------------------------------------------------------------------------------------------------

# Data for test_inventory
# --------------------------------------------------------------------------------------------------------------

LEFT_MENU_COMPONENTS: List[str] = ["All Items", "About", "Logout", "Reset App State"]
ALL_PRICES_FILTER_OPTIONS: List[str] = [
    "Name (A to Z)",
    "Name (Z to A)",
    "Price (low to high)",
    "Price (high to low)",
]
DEFAULT_FILTER_VALUE: str = ALL_PRICES_FILTER_OPTIONS[0]

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

# --------------------------------------------------------------------------------------------------------------

# Data for test_cart
# --------------------------------------------------------------------------------------------------------------

ALL_ITEMS_INDEX: list[int] = [index for index in range(ITEMS_AMOUNT)]

FIRST_ITEM_KEY: str = next(iter(INVENTORY_ITEMS_DATA))

# Cart shows everything inventory does, plus a quantity per item.
CART_ITEMS_DATA: dict[str, dict[str, str]] = {
    name: {**details, "quantity": "1"} for name, details in INVENTORY_ITEMS_DATA.items()
}
CART_ITEM_DATA: dict[str, dict[str, str]] = {
    FIRST_ITEM_KEY: CART_ITEMS_DATA[FIRST_ITEM_KEY]
}

# --------------------------------------------------------------------------------------------------------------
