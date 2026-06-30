"""
Token refresh logic for maintaining active user sessions.
"""

def should_refresh_token(token_age_seconds: int, expiry_threshold: int = 300) -> bool:
    """Determines if a token should be refreshed based on its age."""
    return token_age_seconds >= expiry_threshold


def generate_refresh_payload(user_id: str, current_token: str) -> dict:
    """Builds the payload required to refresh an authentication token."""
    return {
        "user_id": user_id,
        "current_token": current_token,
        "action": "refresh",
    }
