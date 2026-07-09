import re
from typing import Any, Dict, Optional, Tuple, Sized

def validate_value(value: Any, constraints: Dict[str, Any]) -> Tuple[bool, Optional[str]]:
    """
    Validates a given value against a set of specified constraints.

    Args:
        value: The value to be validated.
        constraints: A dictionary where keys are constraint names and values are
                     the constraint parameters. Supported constraints include:
                     - 'type': Expected type (e.g., int, str, float).
                     - 'not_empty': bool (True if value must not be empty/None).
                     - 'min_value': int or float (for numerical values).
                     - 'max_value': int or float (for numerical values).
                     - 'min_length': int (for sized values like strings, lists, dicts).
                     - 'max_length': int (for sized values like strings, lists, dicts).
                     - 'regex': str (regular expression pattern for string values).

    Returns:
        A tuple containing:
        - bool: True if the value passes all constraints, False otherwise.
        - Optional[str]: An error message if validation fails, None otherwise.
    """
    # Type validation
    if 'type' in constraints:
        expected_type = constraints['type']
        if not isinstance(value, expected_type):
            return False, f"Value type mismatch: Expected {expected_type.__name__}, got {type(value).__name__}."

    # Not empty validation
    if constraints.get('not_empty', False):
        if value is None:
            return False, "Value cannot be None."
        # Check for emptiness for common sized types
        if isinstance(value, (str, list, dict, set, tuple)) and not value:
            return False, "Value cannot be empty."

    # Numerical validations (min_value, max_value)
    if any(k in constraints for k in ['min_value', 'max_value']):
        # Ensure value is numeric before applying numerical constraints
        if not isinstance(value, (int, float)):
            return False, f"Cannot apply numerical constraints to non-numeric type {type(value).__name__}."

        if 'min_value' in constraints:
            min_val = constraints['min_value']
            if not isinstance(min_val, (int, float)):
                return False, f"Invalid constraint 'min_value': Expected int or float, got {type(min_val).__name__}."
            if value < min_val:
                return False, f"Value {value} is less than minimum allowed value {min_val}."
        if 'max_value' in constraints:
            max_val = constraints['max_value']
            if not isinstance(max_val, (int, float)):
                return False, f"Invalid constraint 'max_value': Expected int or float, got {type(max_val).__name__}."
            if value > max_val:
                return False, f"Value {value} is greater than maximum allowed value {max_val}."

    # Length validations (min_length, max_length)
    if any(k in constraints for k in ['min_length', 'max_length']):
        # Ensure value is sized before applying length constraints
        if not isinstance(value, Sized):
            return False, f"Cannot apply length constraints to non-sized type {type(value).__name__}."
        
        current_length = len(value)
        if 'min_length' in constraints:
            min_len = constraints['min_length']
            if not isinstance(min_len, int) or min_len < 0:
                return False, f"Invalid constraint 'min_length': Expected a non-negative integer, got {type(min_len).__name__}."
            if current_length < min_len:
                return False, f"Value length {current_length} is less than minimum allowed length {min_len}."
        if 'max_length' in constraints:
            max_len = constraints['max_length']
            if not isinstance(max_len, int) or max_len < 0:
                return False, f"Invalid constraint 'max_length': Expected a non-negative integer, got {type(max_len).__name__}."
            if current_length > max_len:
                return False, f"Value length {current_length} is greater than maximum allowed length {max_len}."

    # Regex validation
    if 'regex' in constraints:
        if not isinstance(value, str):
            return False, f"Cannot apply regex constraint to non-string type {type(value).__name__}."
        pattern = constraints['regex']
        if not isinstance(pattern, str):
            return False, f"Invalid constraint 'regex': Expected a string pattern, got {type(pattern).__name__}."
        try:
            if not re.match(pattern, value):
                return False, f"Value '{value}' does not match required regex pattern '{pattern}'."
        except re.error as e:
            return False, f"Invalid regex pattern provided: {pattern} - {e}"

    return True, None


# --- Example Test Cases ---

# 1. Valid integer within range
# Expected: (True, None)
# print(validate_value(10, {'type': int, 'min_value': 5, 'max_value': 15}))

# 2. Invalid string length and regex pattern mismatch
# Expected: (False, "Value length 3 is less than minimum allowed length 5.") or (False, "Value 'abc' does not match required regex pattern '^[A-Z]+$'.")... depending on order
# print(validate_value("abc", {'type': str, 'min_length': 5, 'regex': r"^[A-Z]+$", 'not_empty': True}))

# 3. Invalid type and None value with not_empty constraint
# Expected: (False, "Value type mismatch: Expected int, got NoneType.") or (False, "Value cannot be None.")
# print(validate_value(None, {'type': int, 'not_empty': True}))