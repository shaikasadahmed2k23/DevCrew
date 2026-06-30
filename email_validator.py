import re

def is_valid_email(email: str) -> bool:
    """Validates if the given string is a properly formatted email address."""
    pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
    return bool(re.match(pattern, email))


def extract_domain(email: str) -> str:
    """Extracts the domain part from an email address."""
    if not is_valid_email(email):
        raise ValueError("Invalid email format")
    return email.split('@')[1]
