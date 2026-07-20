DOCUMENT_TITLE: str = "Swag Labs"
LOGO_TEXT: str = "Swag Labs"

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
SUCCESS_LOGIN_DATA = [(user, PASSWORD) for user in UNLOCKED_USERS]

EMPTY_USERNAME_ERROR: str = "Epic sadface: Username is required"
EMPTY_PASSWORD_ERROR: str = "Epic sadface: Password is required"
WRONG_CREDENTIALS_ERROR: str = (
    "Epic sadface: Username and password do not match any user in this service"
)
LOCKED_ACCOUNT_ERROR: str = "Epic sadface: Sorry, this user has been locked out."

LOGIN_ARGS: str = "user, password"

LOGIN_ERROR_ARGS: str = "user, password"
