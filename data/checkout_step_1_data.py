FIRST_NAME = "test_name"
LAST_NAME = "test_last_name"
ZIP_CODE = "test_zip_code"

EMPTY_FIRST_NAME_ERROR: str = "Error: First Name is required"
EMPTY_LAST_NAME_ERROR: str = "Error: Last Name is required"
EMPTY_ZIP_CODE_ERROR: str = "Error: Postal Code is required"

ACCESS_CHECKOUT_STEP_1_PAGE_WITHOUT_LOGIN_ERROR: str = (
    "Epic sadface: You can only access '/checkout-step-one.html' when you are logged in."
)

# Checkout test case data
CHECKOUT_ARGS: str = "first_name, last_name, zip_code, expected"
CHECKOUT_PARAMS: list[tuple[str, str, str, str]] = [
    ("", LAST_NAME, ZIP_CODE, EMPTY_FIRST_NAME_ERROR),
    (FIRST_NAME, "", ZIP_CODE, EMPTY_LAST_NAME_ERROR),
    (FIRST_NAME, LAST_NAME, "", EMPTY_ZIP_CODE_ERROR),
]
CHECKOUT_IDS: tuple[str, ...] = tuple(x[3] for x in CHECKOUT_PARAMS)
