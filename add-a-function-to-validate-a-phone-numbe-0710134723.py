import re

def validate_phone_number(phone_number: str) -> bool:
    """
    Validates a phone number based on common international formatting and length heuristics.

    This function performs validation by:
    1.  Removing common non-digit separators such as spaces, hyphens, and parentheses.
    2.  Allowing an optional leading '+' character to indicate an international number.
        If '+' is present, it must be the very first character.
    3.  Ensuring that all remaining characters (after handling a leading '+') are digits.
    4.  Checking if the cleaned, digit-only number falls within a plausible length range.
        A typical range for phone numbers globally is between 7 and 15 digits.
        This range is a general heuristic; specific regional requirements might differ.

    Args:
        phone_number: The phone number string to validate.

    Returns:
        True if the phone number adheres to the defined validation rules, False otherwise.
    """
    if not isinstance(phone_number, str) or not phone_number:
        return False

    # 1. Clean up the number: remove spaces, hyphens, and parentheses
    cleaned_number = re.sub(r'[\s\-()]', '', phone_number)

    # 2. Handle an optional leading '+' for international numbers
    has_plus_prefix = cleaned_number.startswith('+')
    if has_plus_prefix:
        digits_only = cleaned_number[1:]  # Get digits after '+'
    else:
        digits_only = cleaned_number

    # 3. Ensure all remaining characters are digits and the string is not empty
    if not digits_only or not digits_only.isdigit():
        return False

    # 4. Check length against common international phone number ranges
    # A general range of 7 to 15 digits is used as a heuristic for plausibility.
    # For example, U.S. numbers are typically 10-11 digits (with country code).
    # Some short local numbers might be 7 digits, and international numbers can be up to 15.
    min_length = 7
    max_length = 15

    return min_length <= len(digits_only) <= max_length


# Example Test Cases:
# print(validate_phone_number("+1 (555) 123-4567"))  # Expected: True (Valid international, formatted)
# print(validate_phone_number("555-123-4567"))       # Expected: True (Valid domestic, formatted)
# print(validate_phone_number("not-a-phone"))        # Expected: False (Contains non-digit characters)
# print(validate_phone_number("123"))                # Expected: False (Too short)
# print(validate_phone_number(""))                   # Expected: False (Empty string)
# print(validate_phone_number(None))                 # Expected: False (Invalid type)