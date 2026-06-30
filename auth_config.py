"""
Authentication configuration constants.
This module defines configuration values used by the authentication system.
No actual secrets are stored here - only configuration structure.
"""

# Token expiry settings (in seconds)
ACCESS_TOKEN_EXPIRY = 3600  # 1 hour
REFRESH_TOKEN_EXPIRY = 604800  # 7 days

# Password policy constants
MIN_PASSWORD_LENGTH = 12
REQUIRE_SPECIAL_CHAR = True
REQUIRE_UPPERCASE = True
REQUIRE_NUMBER = True

# Session settings
MAX_LOGIN_ATTEMPTS = 5
LOCKOUT_DURATION_MINUTES = 15


def get_password_policy_description() -> str:
    """Returns a human-readable description of the password policy."""
    return (
        f"Password must be at least {MIN_PASSWORD_LENGTH} characters, "
        f"include uppercase, a number, and a special character."
    )
