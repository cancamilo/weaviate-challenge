def flatten(nested_list: list) -> list:
    """Flatten a list of lists into a single list."""

    return [item for sublist in nested_list for item in sublist]

def sort_by_distance(results: list) -> list:
    """Sort the results of a list by smallest to largest distance"""
    return sorted(results, key=lambda x: x["distance"])

def remove_duplicates(results: list) -> list:
    """remove duplicated items by uuid"""
    seen = set()
    deduplicated = []
    for item in results:
        if item["uuid"] not in seen:
            deduplicated.append(item)
            seen.add(item["uuid"])

    return deduplicated