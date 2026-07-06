def validate_passport_number(passport_number: str) -> bool:
    """
    Validates a passport number based on common structural requirements.

    This function performs a generic structural validation. It checks for:
    1. The input is indeed a string.
    2. The passport number, after stripping leading/trailing whitespace,
       is not empty.
    3. The cleaned passport number consists only of alphanumeric characters (A-Z, 0-9).
    4. The length of the cleaned passport number is between 6 and 15 characters, inclusive.

    Note: Passport number formats vary significantly by country. This validator
    does NOT implement country-specific rules (e.g., checksums, specific starting
    characters, exact fixed lengths per country). It provides a basic, general
    structure check common to many international travel documents.
    For more rigorous validation, country-specific regex patterns or APIs would be required.

    Args:
        passport_number: The passport number string to validate.

    Returns:
        True if the passport number meets the general structural requirements,
        False otherwise.
    """
    if not isinstance(passport_number, str):
        return False

    # Clean the input: strip whitespace and convert to uppercase for consistent checking
    cleaned_number = passport_number.strip().upper()

    # 1. Check if the string is empty after stripping
    if not cleaned_number:
        return False

    # 2. Check for alphanumeric characters only
    if not cleaned_number.isalnum():
        return False

    # 3. Check for length within a common range
    # Common passport lengths generally fall between 7 and 12 characters.
    # Using 6-15 here for broader applicability to various international formats.
    min_length = 6
    max_length = 15
    if not (min_length <= len(cleaned_number) <= max_length):
        return False

    return True

# Example Test Cases:
# validate_passport_number("123456789")       # Expected: True (Common 9-digit format)
# validate_passport_number("AB1234567")       # Expected: True (Common alphanumeric format)
# validate_passport_number("P12345678901")    # Expected: True (Valid length within range)
# validate_passport_number("12345")           # Expected: False (Too short)
# validate_passport_number("P123456789012345") # Expected: False (Too long)
# validate_passport_number("P12345678!")       # Expected: False (Contains special character)
# validate_passport_number("")                # Expected: False (Empty string)
# validate_passport_number("   ")             # Expected: False (Whitespace only)
# validate_passport_number(None)              # Expected: False (Not a string)
# validate_passport_number(123456789)         # Expected: False (Not a string)