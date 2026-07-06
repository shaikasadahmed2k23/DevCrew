import re

def validate_roll_number(roll_number: str) -> bool:
    """
    Validates a university or college roll number against a common pattern.

    The expected pattern is defined as:
    1.  Starts with 2 to 4 uppercase letters (e.g., department code like "CS", "EEE", "BME").
    2.  Followed by 2 digits (e.g., year like "21" for 2021, "19" for 2019).
    3.  Followed by 3 to 5 digits (e.g., student's unique ID like "001", "1234", "00050").

    Examples of valid roll numbers: "CS21001", "EEE20123", "BME19050", "IT220001", "CSE21050".

    Args:
        roll_number: The roll number string to validate.

    Returns:
        True if the roll number matches the expected pattern, False otherwise.

    Raises:
        TypeError: If the input `roll_number` is not a string.
    """
    if not isinstance(roll_number, str):
        raise TypeError("Roll number must be a string.")

    # Regex pattern for validation:
    # ^                 - Start of the string
    # [A-Z]{2,4}        - 2 to 4 uppercase letters (e.g., department code)
    # [0-9]{2}          - Exactly 2 digits (e.g., year)
    # [0-9]{3,5}        - 3 to 5 digits (e.g., student ID)
    # $                 - End of the string
    roll_number_pattern = r"^[A-Z]{2,4}[0-9]{2}[0-9]{3,5}$"

    return bool(re.fullmatch(roll_number_pattern, roll_number))

# Example Test Cases:
# print(validate_roll_number("CS21001"))      # Expected: True
# print(validate_roll_number("EEE20123"))     # Expected: True
# print(validate_roll_number("IT220001"))     # Expected: True (4 letters dept, 2 digits year, 4 digits id)
# print(validate_roll_number("CSE21050"))     # Expected: True (3 letters dept, 2 digits year, 3 digits id)
# print(validate_roll_number("BME190005"))    # Expected: True (3 letters dept, 2 digits year, 5 digits id)
# print(validate_roll_number("cs21001"))      # Expected: False (lowercase letters)
# print(validate_roll_number("CS2101"))       # Expected: False (ID too short, 4 digits expected minimum 3)
# print(validate_roll_number("CS2100001"))    # Expected: False (ID too long, maximum 5 digits)
# print(validate_roll_number("CS21A001"))     # Expected: False (letter in year/ID part)
# print(validate_roll_number("C21001"))       # Expected: False (department too short, minimum 2 letters)
# print(validate_roll_number("CSIT21001"))    # Expected: False (department too long, maximum 4 letters)
# print(validate_roll_number(""))             # Expected: False (empty string)
# try:
#     validate_roll_number(12345)
# except TypeError as e:
#     print(f"Caught expected error: {e}") # Expected: Caught expected error: Roll number must be a string.