"""
Session and authentication security configuration.
"""

SESSION_TIMEOUT_MINUTES = 30
TOKEN_REFRESH_THRESHOLD_MINUTES = 5
ENABLE_TWO_FACTOR_AUTH = True


def get_session_policy_summary() -> str:
    """Returns a summary of session security settings."""
    return f"Sessions expire after {SESSION_TIMEOUT_MINUTES} minutes of inactivity."
