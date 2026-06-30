def remove_duplicates(items: list) -> list:
    """Removes duplicate items from a list while preserving order."""
    seen = set()
    result = []
    for item in items:
        if item not in seen:
            seen.add(item)
            result.append(item)
    return result


def flatten_list(nested: list) -> list:
    """Flattens a nested list into a single-level list."""
    result = []
    for item in nested:
        if isinstance(item, list):
            result.extend(flatten_list(item))
        else:
            result.append(item)
    return result
