import pytest

from sauce_project.po.pages.checkout_step_1_page import CheckoutStepOnePage

FIRST_NAME = "test_name"
LAST_NAME = "test_last_name"
ZIP_CODE = "test_zip_code"


def test_01_verify_checkout_error_with_empty_first_name(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name="", last_name=LAST_NAME, zip_code=ZIP_CODE
        )
    assert "Error: First Name is required" == str(exception_information.value)


def test_02_verify_checkout_error_with_empty_last_name(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name="", zip_code=ZIP_CODE
        )
    assert "Error: Last Name is required" == str(exception_information.value)


def test_03_verify_checkout_error_with_empty_zip_code(
    checkout_step_1_with_item: CheckoutStepOnePage,
) -> None:
    with pytest.raises(RuntimeError) as exception_information:
        checkout_step_1_with_item.fill_in_checkout_information(
            first_name=FIRST_NAME, last_name=LAST_NAME, zip_code=""
        )
    assert "Error: Postal Code is required" == str(exception_information.value)
