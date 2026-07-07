import re

def is_valid_email(email_address: str) -> bool:
    """
    Checks if a given string is a valid email address using a regular expression.

    This function uses a common regular expression pattern to validate email
    addresses. While not exhaustively compliant with all RFC specifications
    (which would result in an extremely complex regex), it covers most
    practical and common email formats.

    The pattern checks for:
    - A local part (before '@') consisting of alphanumeric characters, dots,
      underscores, percent signs, pluses, or hyphens.
    - An '@' symbol.
    - A domain part consisting of alphanumeric characters, dots, or hyphens.
    - A top-level domain (TLD) of at least two letters.

    Args:
        email_address: The string to be validated as an email address.

    Returns:
        True if the email_address is valid according to the regex pattern,
        False otherwise.
    """
    # A robust but practical regex for email validation
    # This pattern covers most common valid email formats
    # It allows for alphanumeric characters, dots, underscores, percent, plus, and hyphens in the local part
    # It allows for alphanumeric characters, dots, and hyphens in the domain part
    # It requires a TLD of at least two letters
    email_pattern = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    return bool(email_pattern.fullmatch(email_address))

# Example Test Cases:
# print(is_valid_email("test@example.com"))       # Expected: True
# print(is_valid_email("user.name+tag@sub.domain.co.uk")) # Expected: True
# print(is_valid_email("invalid-email"))         # Expected: False
# print(is_valid_email("no@tld"))                # Expected: False
# print(is_valid_email("a@b.c"))                 # Expected: True