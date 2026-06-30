"""
Payment processing configuration constants.
"""

PAYMENT_TIMEOUT_SECONDS = 30
MAX_RETRY_ATTEMPTS = 3
SUPPORTED_CURRENCIES = ["USD", "EUR", "INR"]


def get_payment_policy_summary() -> str:
    """Returns a summary of payment processing settings."""
    return f"Payments timeout after {PAYMENT_TIMEOUT_SECONDS} seconds with {MAX_RETRY_ATTEMPTS} retries."
