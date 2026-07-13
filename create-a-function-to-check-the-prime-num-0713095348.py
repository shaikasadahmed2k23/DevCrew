import math

def is_prime(n: int) -> bool:
    """
    Checks if a given integer is a prime number.

    A prime number is a natural number greater than 1 that has no positive
    divisors other than 1 and itself.

    Args:
        n: The integer to be checked.

    Returns:
        True if n is a prime number, False otherwise.

    Examples:
        is_prime(7)   -> True
        is_prime(10)  -> False
        is_prime(1)   -> False
        is_prime(2)   -> True
        is_prime(0)   -> False
        is_prime(-5)  -> False
    """
    if n <= 1:
        return False
    if n <= 3:  # 2 and 3 are prime numbers
        return True
    if n % 2 == 0 or n % 3 == 0: # Exclude multiples of 2 and 3
        return False

    # All prime numbers greater than 3 can be expressed in the form 6k ± 1.
    # We only need to check divisors up to the square root of n.
    # We can skip checking even numbers and multiples of 3.
    # We start with 5 and check numbers in the form (i) and (i + 2)
    # i.e., 5, 7, 11, 13, 17, 19, ...
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6 # Increment by 6 to check the next 6k ± 1 pair
    return True

# Example test cases:
# print(is_prime(7))    # Expected: True
# print(is_prime(10))   # Expected: False
# print(is_prime(1))    # Expected: False
# print(is_prime(2))    # Expected: True
# print(is_prime(97))   # Expected: True
# print(is_prime(100))  # Expected: False