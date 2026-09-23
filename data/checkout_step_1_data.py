import pytest

from data.login_data import ParameterSet

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
CHECKOUT_PARAMS: list[ParameterSet] = [
    pytest.param(
        "",
        "",
        "",
        EMPTY_FIRST_NAME_ERROR,
        id="all_fields_empty",
    ),
    pytest.param(
        "",
        LAST_NAME,
        ZIP_CODE,
        EMPTY_FIRST_NAME_ERROR,
        id="empty_first_name",
    ),
    pytest.param(
        FIRST_NAME,
        "",
        ZIP_CODE,
        EMPTY_LAST_NAME_ERROR,
        id="empty_last_name",
    ),
    pytest.param(
        FIRST_NAME,
        LAST_NAME,
        "",
        EMPTY_ZIP_CODE_ERROR,
        id="empty_zip_code",
    ),
]

FIRST_NAME_PLACEHOLDER: str = "First Name"
LAST_NAME_PLACEHOLDER: str = "Last Name"
ZIP_CODE_PLACEHOLDER: str = "Zip/Postal Code"
