import re

# Compiled regex for validating email addresses.
# This regex aims for a balance between RFC compliance and practical usability,
# covering most common valid email patterns while rejecting common invalid ones.
#
# Explanation of the regex components:
# ^                                       # Start of the string
# [a-zA-Z0-9._%+-]+                       # Local part:
#                                         #   - Allows alphanumeric characters, dot (.), underscore (_), percent (%), plus (+), hyphen (-)
#                                         #   - Must have at least one character
# @                                       # Separator: '@' symbol
# (?:                                     # Domain part (non-capturing group for repeated labels):
#   [a-zA-Z0-9]                           #   - Each domain label must start with an alphanumeric character
#   (?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?    #   - Followed by 0-61 alphanumeric characters or hyphens, but must end with an alphanumeric character
#                                         #     (This prevents leading/trailing hyphens within labels and ensures labels aren't too long)
#   \.                                    #   - Each label is separated by a literal dot (.)
# )+                                      #   - There must be at least one domain label (e.g., example.com has 'example' and 'com')
# [a-zA-Z]{2,63}                          # Top-level domain (TLD):
#                                         #   - Consists of 2 to 63 alphabetic characters (common length range for TLDs)
# $                                       # End of the string
_EMAIL_REGEX = re.compile(
    r"^[a-zA-Z0-9._%+-]+@(?:[a-zA-Z0-9](?:[a-zA-Z0-9-]{0,61}[a-zA-Z0-9])?\.)+[a-zA-Z]{2,63}$"
)


def is_valid_email(email_address: str) -> bool:
    """
    Checks if a string is a valid email address using a regular expression.

    This function uses a robust regular expression that balances RFC compliance
    with practical usability. It covers most common valid email patterns and
    rejects common invalid ones, checking for the general structure of
    'local-part@domain.tld', including constraints on allowed character sets and
    structural rules within the local part and domain.

    Args:
        email_address (str): The string to validate as an email address.

    Returns:
        bool: True if the string is a valid email address, False otherwise.
    """
    if not isinstance(email_address, str):
        # Ensure the input is a string before attempting regex matching.
        return False

    return bool(_EMAIL_REGEX.fullmatch(email_address))


# Example Test Cases:
# print(is_valid_email("test@example.com"))          # Expected: True
# print(is_valid_email("john.doe@sub.domain.co.uk")) # Expected: True
# print(is_valid_email("user+alias@email.net"))      # Expected: True
# print(is_valid_email("invalid-email"))             # Expected: False (missing @ and domain)
# print(is_valid_email("no@tld"))                    # Expected: False (TLD too short)
# print(is_valid_email("user@.com"))                 # Expected: False (domain part invalid)
# print(is_valid_email("user@domain-.com"))          # Expected: False (domain label ends with hyphen)
# print(is_valid_email("user@domain..com"))          # Expected: False (consecutive dots in domain)