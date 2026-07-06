def is_valid_passport_number(passport_number: str) -> bool:
    """
    Validates a passport number based on common, generic criteria.

    This function provides a general-purpose validation and does not
    enforce country-specific formats, which can vary significantly.
    For specific country validation, a more tailored approach would be
    required.

    Current generic criteria:
    1. The input must be a string.
    2. It must not be empty.
    3. Its length must be between 6 and 20 characters, inclusive.
       (This range covers most common international passport formats,
       e.g., US: 9 digits, UK: 9 digits, Germany: 10 alphanumeric).
    4. It must consist only of alphanumeric characters (letters and numbers).
       No spaces, hyphens, or other special characters are allowed in the
       core number itself.

    Args:
        passport_number: The passport number string to validate.

    Returns:
        True if the passport number meets the generic validation criteria,
        False otherwise.
    """
    if not isinstance(passport_number, str):
        return False

    # Define common length constraints for generic passport numbers
    min_length = 6
    max_length = 20

    # Check for non-emptiness and length range
    if not (min_length <= len(passport_number) <= max_length):
        return False

    # Check if all characters are alphanumeric
    # This excludes spaces, hyphens, and other special characters often
    # found on passport documents but usually not within the core number itself.
    if not passport_number.isalnum():
        return False

    return True


# Example test cases
# print(is_valid_passport_number("ABC12345"))          # Expected: True (Valid length, alphanumeric)
# print(is_valid_passport_number("AB123"))             # Expected: False (Too short)
# print(is_valid_passport_number("AB123-45"))          # Expected: False (Contains non-alphanumeric character '-')