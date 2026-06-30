def reverse_string(text: str) -> str:
    """Reverses the given string."""
    return text[::-1]


def is_palindrome(text: str) -> bool:
    """Checks if the given string is a palindrome (ignoring case and spaces)."""
    cleaned = text.replace(" ", "").lower()
    return cleaned == cleaned[::-1]


def count_vowels(text: str) -> int:
    """Counts the number of vowels in the given string."""
    vowels = "aeiouAEIOU"
    return sum(1 for char in text if char in vowels)
