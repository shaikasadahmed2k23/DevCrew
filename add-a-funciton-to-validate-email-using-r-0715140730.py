import re

def validate_email(email_address: str) -> bool:
    """
    Validates an email address using a regular expression.

    This function checks if the provided string conforms to a common email
    address format. It ensures there is a user part, an '@' symbol,
    and a domain part with at least two characters after the final dot.

    The regex used is generally considered robust for a wide range of
    valid email addresses while still filtering out many invalid formats.
    It may not cover all edge cases defined by RFCs but is suitable for
    most common application requirements.

    Args:
        email_address: The string representing the email address to validate.

    Returns:
        True if the email address is valid, False otherwise.
    """
    # A robust regex for email validation.
    # It covers common patterns:
    # - User part: alphanumeric, plus ., _, %, +, -
    # - Domain part: alphanumeric, plus ., -
    # - Top-level domain: at least two alphabetic characters
    email_regex = r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$"

    # re.fullmatch ensures that the entire string matches the pattern,
    # not just a substring.
    if re.fullmatch(email_regex, email_address):
        return True
    return False

# Example test cases:
# print(validate_email("test@example.com"))       # Expected: True
# print(validate_email("invalid-email"))         # Expected: False
# print(validate_email("user.name+tag@sub.domain.co.uk")) # Expected: True
# print(validate_email("no@.com"))                # Expected: False (domain cannot start with dot)
# print(validate_email("user@domain"))           # Expected: False (missing TLD)