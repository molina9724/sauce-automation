import os
from typing import cast

import pytest
from _pytest.mark.structures import ParameterSet
from dotenv import load_dotenv

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

WRONG_USERNAME: str = "wrong_username"

load_dotenv()
PASSWORD: str = cast(str, os.getenv("PASSWORD"))
if not PASSWORD:
    raise RuntimeError("PASSWORD is missing from the environment")
WRONG_PASSWORD = "wrong_password"

EXPECTED_LOGIN_USERNAMES = list(ALL_USERS)
SUCCESS_LOGIN_DATA = [(user, PASSWORD) for user in UNLOCKED_USERS]

EMPTY_USERNAME_ERROR: str = "Epic sadface: Username is required"
EMPTY_PASSWORD_ERROR: str = "Epic sadface: Password is required"
WRONG_CREDENTIALS_ERROR: str = (
    "Epic sadface: Username and password do not match any user in this service"
)
LOCKED_ACCOUNT_ERROR: str = "Epic sadface: Sorry, this user has been locked out."

LOGIN_ARGS: str = "user, password"

LOGIN_ERROR_ARGS: str = "user, password, error"
LOGIN_ERROR_PARAMS: list[ParameterSet] = [
    # Empty field cases
    pytest.param("", "", EMPTY_USERNAME_ERROR, id="both_fields_empty"),
    pytest.param(DEFAULT_UNLOCKED_USER, "", EMPTY_PASSWORD_ERROR, id="empty_password"),
    pytest.param("", PASSWORD, EMPTY_USERNAME_ERROR, id="empty_username"),
    # Wrong credentials cases
    pytest.param(
        DEFAULT_UNLOCKED_USER,
        WRONG_PASSWORD,
        WRONG_CREDENTIALS_ERROR,
        id="valid_user_wrong_password",
    ),
    pytest.param(
        WRONG_USERNAME,
        PASSWORD,
        WRONG_CREDENTIALS_ERROR,
        id="wrong_user_valid_password",
    ),
    pytest.param(
        WRONG_USERNAME,
        WRONG_PASSWORD,
        WRONG_CREDENTIALS_ERROR,
        id="both_credentials_wrong",
    ),
    # Locked account cases
    pytest.param(
        DEFAULT_BLOCKED_USER,
        PASSWORD,
        LOCKED_ACCOUNT_ERROR,
        id="locked_user_valid_password",
    ),
    pytest.param(
        DEFAULT_BLOCKED_USER, "", EMPTY_PASSWORD_ERROR, id="locked_user_empty_password"
    ),
    pytest.param(
        DEFAULT_BLOCKED_USER,
        WRONG_PASSWORD,
        WRONG_CREDENTIALS_ERROR,
        id="locked_user_wrong_password_hides_status",
    ),
]

USERNAME_PLACEHOLDER: str = "Username"
PASSWORD_PLACEHOLDER: str = "Password"

TYPE: str = "type"
PASSWORD_INPUT_TYPE = "password"
