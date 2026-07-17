import re

def validate_indian_phonenumber(phone_number_str: str) -> bool:
    """
    Validates if a given string represents a valid Indian mobile phone number.

    A valid Indian mobile number typically adheres to the following rules:
    - It must be 10 digits long.
    - It must start with a digit from 6, 7, 8, or 9.
    - It may optionally include:
        - A country code prefix (+91 or 0091), potentially followed by spaces or hyphens.
        - A national dialing prefix (0), potentially followed by spaces or hyphens.
      These prefixes are considered mutually exclusive in common valid dialing formats.

    Args:
        phone_number_str: The phone number string to validate.

    Returns:
        True if the phone number is valid, False otherwise.
    """
    if not isinstance(phone_number_str, str):
        return False

    # Regex pattern for Indian mobile numbers, allowing different valid prefixes and formats.
    # It consists of two main patterns ORed together using the `|` operator.
    # Each pattern implicitly includes the case where no prefix is present.
    #
    # Pattern 1: Optional country code prefix (+91 or 0091) followed by the 10-digit number.
    # ^                                    # Start of the string
    # (?:                                  #   Optional non-capturing group for country code prefix
    #   (?:                                #     Non-capturing group for '+' or '00'
    #     \+                               #       Matches literal '+'
    #     |                                #       OR
    #     00                               #       Matches '00'
    #   )
    #   91                                 #     Matches '91'
    #   [\s\-]*                            #     Matches zero or more spaces or hyphens
    # )?                                   #   End of optional country code prefix group
    # [6789]                               # Number must start with 6, 7, 8, or 9
    # \d{9}                                # Followed by exactly 9 more digits
    # $                                    # End of the string
    #
    # OR
    #
    # Pattern 2: Optional national dialing prefix (0) followed by the 10-digit number.
    # ^                                    # Start of the string
    # (?:                                  #   Optional non-capturing group for '0' prefix
    #   0                                  #     Matches literal '0'
    #   [\s\-]*                            #     Matches zero or more spaces or hyphens
    # )?                                   #   End of optional '0' prefix group
    # [6789]                               # Number must start with 6, 7, 8, or 9
    # \d{9}                                # Followed by exactly 9 more digits
    # $                                    # End of the string
    pattern = (
        r"^(?:(?:\+|00)91[\s\-]*)?[6789]\d{9}$|"  # Validates with optional +91 or 0091 prefix
        r"^(?:0[\s\-]*)?[6789]\d{9}$"             # Validates with optional 0 prefix for national dialing
    )

    return re.fullmatch(pattern, phone_number_str) is not None

# Example Test Cases:
# validate_indian_phonenumber("9876543210")         # Expected: True (Canonical 10-digit number)
# validate_indian_phonenumber("+91 9876543210")     # Expected: True (With country code and space)
# validate_indian_phonenumber("0-9876543210")       # Expected: True (With national '0' prefix and hyphen)
# validate_indian_phonenumber("5123456789")         # Expected: False (Invalid starting digit '5')