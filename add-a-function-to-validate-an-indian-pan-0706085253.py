import re
from typing import Optional

def validate_indian_pan(pan_number: str) -> Optional[str]:
    """
    Validates an Indian PAN card number and returns the card holder type.

    An Indian PAN card number is a 10-character alphanumeric string with the
    format AAAAA0000A, where:
    - The first five characters are alphabetic (uppercase).
    - The next four characters are numeric.
    - The tenth (last) character is alphabetic (uppercase).

    The fourth character of the PAN indicates the card holder type.

    Args:
        pan_number: The PAN card number string to validate.

    Returns:
        The type of the PAN card holder (e.g., "Individual (Person)", "Company")
        if the PAN is valid and its holder type can be determined, otherwise None.
    """

    if not isinstance(pan_number, str):
        return None

    # Convert to uppercase to standardize for validation, as PANs are typically uppercase.
    pan_number = pan_number.upper()

    # Regular expression for PAN card format:
    # ^          - Matches the start of the string.
    # [A-Z]{5}   - Matches exactly five uppercase alphabetic characters.
    # [0-9]{4}   - Matches exactly four numeric digits.
    # [A-Z]{1}   - Matches exactly one uppercase alphabetic character.
    # $          - Matches the end of the string.
    pan_regex = r"^[A-Z]{5}[0-9]{4}[A-Z]{1}$"

    if not re.fullmatch(pan_regex, pan_number):
        # The PAN number does not match the required format.
        return None

    # Define the mapping for the 4th character to PAN holder type.
    # These are standard types used by the Indian Income Tax Department.
    holder_types_map = {
        'P': "Individual (Person)",
        'C': "Company",
        'H': "HUF (Hindu Undivided Family)",
        'A': "AOP (Association of Persons)",
        'B': "BOI (Body of Individuals)",
        'G': "Government",
        'J': "Artificial Juridical Person",
        'L': "Local Authority",
        'F': "Firm",
        'T': "Trust",
    }

    # The 4th character (at index 3, 0-indexed) determines the holder type.
    fourth_char = pan_number[3]

    # Return the holder type if the 4th character is recognized in our map.
    # If the 4th character is not found in `holder_types_map` (even if it's an
    # alphabet and passes regex), it implies an unknown or non-standard PAN type
    # for which we cannot determine the holder type, thus returning None.
    return holder_types_map.get(fourth_char, None)


# Example Test Cases:
# print(validate_indian_pan("ABCPA1234A")) # Expected: "Individual (Person)"
# print(validate_indian_pan("ABCCC1234Z")) # Expected: "Company"
# print(validate_indian_pan("ABCHH5678Q")) # Expected: "HUF (Hindu Undivided Family)"
# print(validate_indian_pan("XYZTA0000X")) # Expected: "Trust"
# print(validate_indian_pan("ABCDE1234F")) # Expected: "Firm"
# print(validate_indian_pan("ABCPA1234"))  # Expected: None (invalid length)
# print(validate_indian_pan("123PA1234A")) # Expected: None (alphabetic chars missing)
# print(validate_indian_pan("ABCPAA123A")) # Expected: None (numeric chars missing)
# print(validate_indian_pan("abcpz1234a")) # Expected: "Individual (Person)" (handles lowercase)
# print(validate_indian_pan("ABCXZ1234A")) # Expected: None (valid format but 'X' is not a recognized 4th char type)
# print(validate_indian_pan(None))        # Expected: None (invalid input type)
# print(validate_indian_pan(""))          # Expected: None (empty string, invalid length)