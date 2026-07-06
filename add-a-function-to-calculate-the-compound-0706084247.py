def calculate_compound_interest(
    principal: float,
    rate: float,
    time: float,
    n_compounded_per_year: int
) -> float:
    """
    Calculates the future value of an investment using the compound interest formula.

    The formula used is: A = P * (1 + R/N)^(N*T)
    Where:
        A = the future value of the investment/loan, including interest
        P = the principal investment amount (the initial deposit or loan amount)
        R = the annual interest rate (as a decimal)
        N = the number of times that interest is compounded per year
        T = the time the money is invested or borrowed for, in years

    Args:
        principal (float): The initial principal amount (P). Must be non-negative.
        rate (float): The annual interest rate (R), expressed as a decimal (e.g., 0.05 for 5%). Must be non-negative.
        time (float): The time the money is invested or borrowed for (T), in years. Must be non-negative.
        n_compounded_per_year (int): The number of times interest is compounded per year (N). Must be a positive integer.

    Returns:
        float: The future value of the investment (A), including principal and accumulated interest.

    Raises:
        ValueError: If any input argument is invalid (e.g., negative principal,
                    negative rate, negative time, or non-positive compounding frequency).
        OverflowError: If the calculation results in a number too large to represent.
        RuntimeError: For any other unexpected errors during the calculation.
    """
    # Input validation
    if not isinstance(principal, (int, float)) or principal < 0:
        raise ValueError("Principal must be a non-negative number.")
    if not isinstance(rate, (int, float)) or rate < 0:
        raise ValueError("Rate must be a non-negative number.")
    if not isinstance(time, (int, float)) or time < 0:
        raise ValueError("Time must be a non-negative number.")
    if not isinstance(n_compounded_per_year, int) or n_compounded_per_year <= 0:
        raise ValueError("Number of times compounded per year must be a positive integer.")

    try:
        # Calculate the base of the exponent: (1 + R/N)
        base = 1 + (rate / n_compounded_per_year)

        # Calculate the exponent: (N*T)
        exponent = n_compounded_per_year * time

        # Calculate the future value: A = P * (base ^ exponent)
        future_value = principal * (base ** exponent)
    except OverflowError:
        raise OverflowError("Calculation resulted in a number too large to represent.")
    except Exception as e:
        # Catch any other unexpected errors during calculation
        raise RuntimeError(f"An unexpected error occurred during compound interest calculation: {e}")

    return future_value

# Example Test Cases:
# 1. Principal: $1000, Rate: 5% (0.05), Time: 10 years, Compounded: Quarterly (4 times/year)
#    Expected: $1643.619462...
#    print(f"Test Case 1: {calculate_compound_interest(1000, 0.05, 10, 4):.4f}") # Output: 1643.6195

# 2. Principal: $5000, Rate: 3% (0.03), Time: 5 years, Compounded: Annually (1 time/year)
#    Expected: $5796.370427...
#    print(f"Test Case 2: {calculate_compound_interest(5000, 0.03, 5, 1):.4f}") # Output: 5796.3704

# 3. Principal: $200, Rate: 7% (0.07), Time: 2 years, Compounded: Monthly (12 times/year)
#    Expected: $229.742323...
#    print(f"Test Case 3: {calculate_compound_interest(200, 0.07, 2, 12):.4f}") # Output: 229.7423