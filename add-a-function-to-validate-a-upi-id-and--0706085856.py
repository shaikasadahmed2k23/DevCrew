import re
from typing import Optional

def validate_upi_id(upi_id: str) -> Optional[str]:
    """
    Validates a UPI ID and returns the associated Payment Service Provider (PSP) handle.

    A UPI ID typically follows the format 'user_name@psp_handle'.
    This function checks for a valid structure and common character sets for
    both the user_name and psp_handle components.

    Validation Rules:
    - The UPI ID must contain exactly one '@' symbol.
    - The part before '@' (user_name) must not be empty and can contain
      alphanumeric characters, dots (.), and hyphens (-).
    - The part after '@' (psp_handle) must not be empty and can contain
      only alphanumeric characters.

    Args:
        upi_id: The UPI ID string to validate.

    Returns:
        The string representing the Payment Service Provider (PSP) handle if the
        UPI ID is valid, otherwise None.
    """
    # Regex pattern for a valid UPI ID:
    # ^[a-zA-Z0-9.-]+   : User part - starts with one or more alphanumeric, dot, or hyphen characters.
    # @                 : The literal '@' separator.
    # [a-zA-Z0-9]+$     : PSP handle - consists of one or more alphanumeric characters, and ends the string.
    upi_pattern = re.compile(r"^[a-zA-Z0-9.-]+@[a-zA-Z0-9]+$")

    if upi_pattern.match(upi_id):
        # If the pattern matches, the UPI ID is structurally valid.
        # The PSP handle is the part after the '@' symbol.
        _, psp_handle = upi_id.split('@', 1)
        return psp_handle
    else:
        # If the pattern does not match, the UPI ID is invalid.
        return None

# Example test cases:
# print(validate_upi_id("john.doe@sbi"))          # Expected: "sbi"
# print(validate_upi_id("jane-smith.123@ybl"))    # Expected: "ybl"
# print(validate_upi_id("invalid@id.format"))     # Expected: None (PSP handle cannot contain dots)
# print(validate_upi_id("no-at-sign-here"))       # Expected: None