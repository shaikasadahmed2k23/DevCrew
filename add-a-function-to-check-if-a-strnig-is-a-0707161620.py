import re

def is_valid_email(email_address: str) -> bool:
    """
    Checks if a given string is a valid email address using a regular expression.

    This function employs a common regular expression pattern to validate email
    addresses. While no regex can perfectly validate every edge case defined
    by RFCs (especially internationalized domain names or quoted local parts),
    this pattern covers the vast majority of commonly accepted email formats.

    The pattern used:
    - Allows alphanumeric characters, dots, underscores, percentage signs,
      plus signs, and hyphens in the local part (before the '@').
    - Requires an '@' symbol.
    - Allows alphanumeric characters, dots, and hyphens in the domain part.
    - Requires at least one dot in the domain part, followed by a top-level
      domain (TLD) consisting of at least two alphabetic characters.

    Args:
        email_address: The string to be checked for email validity.

    Returns:
        True if the string is a valid email address according to the regex pattern,
        False otherwise.
    """
    # Regex pattern for a common email format.
    # It covers most standard email addresses but not all RFC-compliant edge cases
    # (e.g., email addresses with quoted local parts or IP literal domains).
    email_regex = re.compile(r"^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$")

    return bool(email_regex.fullmatch(email_address))

# Example Test Cases (uncomment to run)
# print(f"'test@example.com' is valid: {is_valid_email('test@example.com')}")
# print(f"'john.doe@sub.example.co.uk' is valid: {is_valid_email('john.doe@sub.example.co.uk')}")
# print(f"'invalid-email' is valid: {is_valid_email('invalid-email')}")
# print(f"'user@domain' is valid: {is_valid_email('user@domain')}") # Invalid: missing TLD
# print(f"'user@.com' is valid: {is_valid_email('user@.com')}") # Invalid: domain starts with dot or empty domain part before dot