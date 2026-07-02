from sauce_project.po.pages.base_page import INVENTORY_URL

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
