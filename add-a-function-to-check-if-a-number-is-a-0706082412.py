def is_armstrong(number: int) -> bool:
    """
    Checks if a given integer is an Armstrong number.

    An Armstrong number (also known as a narcissistic number, pluperfect digital
    invariant, or perfect digital invariant) is a number that is the sum of its
    own digits each raised to the power of the number of digits.

    For example:
    - 0-9 are considered Armstrong numbers (e.g., 3 = 3^1).
    - 153 is an Armstrong number (1^3 + 5^3 + 3^3 = 1 + 125 + 27 = 153).
    - 1634 is an Armstrong number (1^4 + 6^4 + 3^4 + 4^4 = 1 + 1296 + 81 + 256 = 1634).

    Args:
        number: An integer to check.

    Returns:
        True if the number is an Armstrong number, False otherwise.
    """
    if number < 0:
        return False
    
    # Convert the number to a string to easily access its digits and count them
    num_str = str(number)
    num_digits = len(num_str)
    
    sum_of_powers = 0
    for digit_char in num_str:
        digit = int(digit_char)
        sum_of_powers += digit ** num_digits
        
    return sum_of_powers == number

# Example test cases:
# print(is_armstrong(153))  # Expected: True
# print(is_armstrong(9))    # Expected: True (single digit numbers are Armstrong)
# print(is_armstrong(123))  # Expected: False
# print(is_armstrong(0))    # Expected: True (0 is 0^1 = 0)
# print(is_armstrong(-1))   # Expected: False